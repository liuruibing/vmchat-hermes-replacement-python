from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional, Set, Union
from jsonschema import Draft7Validator, FormatChecker
from pydantic import BaseModel, Field

from app.compatibility.hermes_request import VmReportDsl
from app.contracts.types import ValidationFailure, ValidationIssue, ValidationResult, ValidationSuccess


class ValidateOptions(BaseModel):
    catalogContract: Optional[Dict[str, Any]] = Field(default=None, alias="catalog_contract")
    schemaJson: Optional[Dict[str, Any]] = Field(default=None, alias="schema_json")
    currentBlockIds: Optional[List[str]] = Field(default=None, alias="current_block_ids")

    model_config = {"populate_by_name": True}


FORBIDDEN_TOKENS: Set[str] = {
    "window",
    "document",
    "fetch",
    "XMLHttpRequest",
    "localStorage",
    "sessionStorage",
    "globalThis",
    "self",
    "Function",
    "eval",
}


def escape_reg_exp(val: str) -> str:
    return re.escape(str(val))


def source_writes_field(source: str, field: str) -> bool:
    escaped_field = escape_reg_exp(field)
    object_property_pattern = re.compile(rf"(?:^|[,{{}}]\s*){escaped_field}\s*:", re.MULTILINE)
    assigned_property_pattern = re.compile(
        rf"(?:\.\s*{escaped_field}\b|\[\s*['\"]{escaped_field}['\"]\s*\])\s*="
    )
    return bool(object_property_pattern.search(source) or assigned_property_pattern.search(source))


def validate_date_range(begin_date: Any, end_date: Any) -> None:
    begin_str = str(begin_date or "").replace("-", "")
    end_str = str(end_date or "").replace("-", "")
    values = [
        ("开始日期", begin_str),
        ("结束日期", end_str),
    ]
    for label, digits in values:
        if not re.match(r"^\d{8}$", digits):
            raise ValueError(f"{label} 必须为 YYYYMMDD 或 YYYY-MM-DD")
        year = int(digits[0:4])
        month = int(digits[4:6])
        day = int(digits[6:8])
        try:
            parsed = datetime(year, month, day, tzinfo=timezone.utc)
            if parsed.year != year or parsed.month != month or parsed.day != day:
                raise ValueError
        except Exception:
            raise ValueError(f"{label} 不是有效日期")

    if values[0][1] > values[1][1]:
        raise ValueError("开始日期不得晚于结束日期")


def validate_format(fmt: Any, label: str) -> None:
    if not isinstance(fmt, dict):
        raise ValueError(f"{label} 必须是对象")
    allowed_types = ["raw", "text", "date", "decimal", "percentage"]
    fmt_type = str(fmt.get("type"))
    if fmt_type not in allowed_types:
        raise ValueError(f"{label} 使用了不支持的格式化类型：{fmt.get('type')}")

    digits = fmt.get("digits")
    if digits is not None:
        if type(digits) is not int or digits < 0:
            raise ValueError(f"{label}.digits 必须是非负整数")

    if "multiplier" in fmt:
        raise ValueError(f"{label}.multiplier 已禁用；数值换算必须只在 transform.function 中执行一次")

    for prop in ["prefix", "suffix", "nullValue"]:
        if prop in fmt and fmt[prop] is not None and not isinstance(fmt[prop], str):
            raise ValueError(f"{label}.{prop} 必须是字符串")


def parse_js_tokens(source: str) -> List[str]:
    i = 0
    n = len(source)
    stack: List[str] = []
    identifiers: List[str] = []

    while i < n:
        ch = source[i]

        # Single-line comment
        if ch == "/" and i + 1 < n and source[i + 1] == "/":
            i += 2
            while i < n and source[i] != "\n":
                i += 1
            continue

        # Multi-line comment
        if ch == "/" and i + 1 < n and source[i + 1] == "*":
            i += 2
            comment_closed = False
            while i + 1 < n:
                if source[i] == "*" and source[i + 1] == "/":
                    i += 2
                    comment_closed = True
                    break
                i += 1
            if not comment_closed:
                raise ValueError("Unclosed multi-line comment")
            continue

        # String literal (single or double quote)
        if ch in ("'", '"'):
            quote = ch
            i += 1
            str_closed = False
            while i < n:
                if source[i] == "\\":
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    str_closed = True
                    break
                if source[i] == "\n" and quote != "`":
                    raise ValueError(f"Unclosed string literal ({quote})")
                i += 1
            if not str_closed:
                raise ValueError(f"Unclosed string literal ({quote})")
            continue

        # Template literal
        if ch == "`":
            i += 1
            str_closed = False
            while i < n:
                if source[i] == "\\":
                    i += 2
                    continue
                if source[i] == "`":
                    i += 1
                    str_closed = True
                    break
                if source[i] == "$" and i + 1 < n and source[i + 1] == "{":
                    stack.append("`")
                    i += 2
                    break
                i += 1
            if not str_closed and (not stack or stack[-1] != "`"):
                raise ValueError("Unclosed template literal")
            continue

        # Brackets / Parens / Braces
        if ch in "({[":
            stack.append(ch)
            i += 1
            continue
        elif ch in ")}]":
            if not stack:
                raise ValueError(f"Unexpected closing bracket: {ch}")
            top = stack.pop()
            if top == "`" and ch == "}":
                continue
            matching = {"(": ")", "{": "}", "[": "]"}
            if matching.get(top) != ch:
                raise ValueError(f"Mismatched bracket: expected {matching.get(top)}, got {ch}")
            i += 1
            continue

        # Identifier
        if ch.isalpha() or ch in "_$":
            start = i
            while i < n and (source[i].isalnum() or source[i] in "_$"):
                i += 1
            ident = source[start:i]
            identifiers.append(ident)
            continue

        i += 1

    if stack:
        raise ValueError("Unclosed bracket or brace")

    return identifiers


def check_js_ast(node_source: str, path_prefix: str) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    try:
        identifiers = parse_js_tokens(node_source)
        for ident in identifiers:
            if ident in FORBIDDEN_TOKENS:
                issues.append(
                    ValidationIssue(
                        code="FORBIDDEN_IDENTIFIER",
                        path=path_prefix,
                        message=f"transform.function 不得包含禁用 Token 或全局对象：{ident}",
                    )
                )
    except Exception as err:
        issues.append(
            ValidationIssue(
                code="ACORN_PARSE_ERROR",
                path=path_prefix,
                message=f"transform.function 无法编译: {err}",
            )
        )
    return issues


def validate_vm_report_dsl_set(
    input_data: Any,
    options: Optional[Union[ValidateOptions, Dict[str, Any]]] = None,
    catalog_contract: Optional[Dict[str, Any]] = None,
    schema_json: Optional[Dict[str, Any]] = None,
    current_block_ids: Optional[List[str]] = None,
    **kwargs: Any,
) -> ValidationResult:
    issues: List[ValidationIssue] = []

    opts_catalog = catalog_contract
    opts_schema = schema_json
    opts_block_ids = current_block_ids

    if options is not None:
        if isinstance(options, dict):
            if opts_catalog is None:
                opts_catalog = options.get("catalogContract") or options.get("catalog_contract")
            if opts_schema is None:
                opts_schema = options.get("schemaJson") or options.get("schema_json")
            if opts_block_ids is None:
                opts_block_ids = options.get("currentBlockIds") or options.get("current_block_ids")
        elif isinstance(options, ValidateOptions):
            if opts_catalog is None:
                opts_catalog = options.catalogContract
            if opts_schema is None:
                opts_schema = options.schemaJson
            if opts_block_ids is None:
                opts_block_ids = options.currentBlockIds
        elif hasattr(options, "__dict__"):
            if opts_catalog is None:
                opts_catalog = getattr(options, "catalogContract", None) or getattr(
                    options, "catalog_contract", None
                )
            if opts_schema is None:
                opts_schema = getattr(options, "schemaJson", None) or getattr(
                    options, "schema_json", None
                )
            if opts_block_ids is None:
                opts_block_ids = getattr(options, "currentBlockIds", None) or getattr(
                    options, "current_block_ids", None
                )

    if not input_data:
        return ValidationFailure(
            ok=False,
            errors=[
                ValidationIssue(
                    code="INVALID_INPUT", path="/", message="DSL 必须是对象或非空数组"
                )
            ],
        )

    dsls_raw: List[Any] = []
    if isinstance(input_data, list):
        if len(input_data) == 0:
            return ValidationFailure(
                ok=False,
                errors=[
                    ValidationIssue(
                        code="EMPTY_DSL_ARRAY", path="/", message="DSL 数组不能为空"
                    )
                ],
            )
        dsls_raw = input_data
    elif isinstance(input_data, dict):
        dsls_raw = [input_data]
    elif isinstance(input_data, BaseModel):
        dsls_raw = [input_data.model_dump(by_alias=True)]
    else:
        return ValidationFailure(
            ok=False,
            errors=[
                ValidationIssue(
                    code="INVALID_INPUT", path="/", message="DSL 必须是对象或数组"
                )
            ],
        )

    # Context-aware target validation using current_block_ids
    if opts_block_ids is not None:
        valid_current_ids = set(opts_block_ids)

        if isinstance(input_data, list):
            returned_set: Set[str] = set()
            for i, item_obj in enumerate(dsls_raw):
                item = item_obj.model_dump(by_alias=True) if isinstance(item_obj, BaseModel) else item_obj
                item_action = item.get("action") if isinstance(item, dict) else None
                if item_action != "update":
                    issues.append(
                        ValidationIssue(
                            code="BATCH_ACTION_MUST_BE_UPDATE",
                            path=f"/[{i}]",
                            message="批量修改 DSL 的 action 必须为 update",
                        )
                    )
                item_target_id = (
                    (item.get("targetBlockId") or item.get("id") or "")
                    if isinstance(item, dict)
                    else ""
                )
                if item_target_id not in valid_current_ids:
                    issues.append(
                        ValidationIssue(
                            code="BATCH_EXTRA_TARGET",
                            path=f"/[{i}]",
                            message=f"批量修改 DSL 包含了未在当前报表块中的目标 ID: {item_target_id}",
                        )
                    )
                if item_target_id in returned_set:
                    issues.append(
                        ValidationIssue(
                            code="BATCH_DUPLICATE_TARGET",
                            path=f"/[{i}]",
                            message=f"批量修改 DSL 目标 ID 重复: {item_target_id}",
                        )
                    )
                returned_set.add(item_target_id)
        else:
            item_obj = dsls_raw[0]
            item = item_obj.model_dump(by_alias=True) if isinstance(item_obj, BaseModel) else item_obj
            if isinstance(item, dict) and item.get("action") == "update":
                item_target_id = item.get("targetBlockId") or item.get("id") or ""
                if item_target_id not in valid_current_ids:
                    issues.append(
                        ValidationIssue(
                            code="UPDATE_TARGET_NOT_FOUND",
                            path="/id",
                            message=f"update 目标 ID '{item_target_id}' 未在当前报表块中找到",
                        )
                    )

    # Schema Json Validator
    schema_validator: Optional[Draft7Validator] = None
    if opts_schema:
        try:
            Draft7Validator.check_schema(opts_schema)
            schema_validator = Draft7Validator(opts_schema, format_checker=FormatChecker())
        except Exception as err:
            raise ValueError(f"INVALID_SCHEMA: Failed to compile schemaJson: {err}")

    dsls_success: List[Any] = []

    for index, dsl_obj in enumerate(dsls_raw):
        path_prefix = f"/[{index}]" if len(dsls_raw) > 1 else ""

        if isinstance(dsl_obj, BaseModel):
            dsl = dsl_obj.model_dump(by_alias=True)
        elif isinstance(dsl_obj, dict):
            dsl = dsl_obj
        else:
            issues.append(
                ValidationIssue(
                    code="INVALID_DSL_OBJECT",
                    path=path_prefix or "/",
                    message="DSL 必须是对象",
                )
            )
            continue

        dsls_success.append(dsl)

        # Step 1: Schema validation for all DSLs (normalizing legacy params out)
        if schema_validator:
            excluded_keys = {
                "targetBlockId",
                "title",
                "params",
                "pendingMappings",
                "resolvedParams",
                "fieldMappings",
            }
            struct_check_dsl = {k: v for k, v in dsl.items() if k not in excluded_keys}
            for err in schema_validator.iter_errors(struct_check_dsl):
                instance_path = ""
                for p in err.path:
                    instance_path += f"/{p}"
                issues.append(
                    ValidationIssue(
                        code="AJV_SCHEMA_ERROR",
                        path=f"{path_prefix}{instance_path}",
                        message=f"DSL Schema 校验失败: {err.message}",
                    )
                )

        if "status" in dsl:
            issues.append(
                ValidationIssue(
                    code="DEPRECATED_STATUS",
                    path=f"{path_prefix}/status",
                    message="DSL 不再使用 status，请使用 action",
                )
            )

        action_val = dsl.get("action")
        if action_val not in ["create", "update"]:
            issues.append(
                ValidationIssue(
                    code="INVALID_ACTION",
                    path=f"{path_prefix}/action",
                    message="顶层 action 只能为 create 或 update",
                )
            )

        dsl_id = dsl.get("id")
        if not dsl_id or not isinstance(dsl_id, str):
            issues.append(
                ValidationIssue(
                    code="MISSING_ID",
                    path=f"{path_prefix}/id",
                    message="顶层 id 必须是有效字符串",
                )
            )
        elif not re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            dsl_id,
            re.IGNORECASE,
        ):
            issues.append(
                ValidationIssue(
                    code="INVALID_UUID",
                    path=f"{path_prefix}/id",
                    message="顶层 id 必须是有效 UUID",
                )
            )

        for prop in ["pendingMappings", "resolvedParams", "fieldMappings"]:
            if prop in dsl:
                issues.append(
                    ValidationIssue(
                        code="FORBIDDEN_PROPERTY",
                        path=f"{path_prefix}/{prop}",
                        message=f"DSL 不允许 {prop}",
                    )
                )

        # Params validation (legacy)
        if "params" in dsl:
            p = dsl.get("params")
            if not isinstance(p, dict):
                issues.append(
                    ValidationIssue(
                        code="INVALID_PARAMS",
                        path=f"{path_prefix}/params",
                        message="DSL 顶层 params 必须是对象",
                    )
                )
            else:
                try:
                    if p.get("beginDate") or p.get("endDate"):
                        validate_date_range(p.get("beginDate"), p.get("endDate"))
                except Exception as err:
                    issues.append(
                        ValidationIssue(
                            code="INVALID_DATE_RANGE",
                            path=f"{path_prefix}/params",
                            message=str(err),
                        )
                    )

        # Requests validation
        request_ids: Set[str] = set()
        requests = dsl.get("requests")
        if not isinstance(requests, list) or len(requests) == 0:
            issues.append(
                ValidationIssue(
                    code="MISSING_REQUESTS",
                    path=f"{path_prefix}/requests",
                    message="DSL 必须包含 requests",
                )
            )
        else:
            for r_idx, req in enumerate(requests):
                req_path = f"{path_prefix}/requests[{r_idx}]"
                if not isinstance(req, dict):
                    issues.append(
                        ValidationIssue(
                            code="INVALID_REQUEST",
                            path=req_path,
                            message="request 必须是对象",
                        )
                    )
                    continue

                req_id = req.get("id") or f"req-{r_idx + 1}"
                if req_id in request_ids:
                    issues.append(
                        ValidationIssue(
                            code="DUPLICATE_REQUEST_ID",
                            path=f"{req_path}/id",
                            message=f"request id 重复：{req_id}",
                        )
                    )
                request_ids.add(req_id)

                if "type" in req:
                    issues.append(
                        ValidationIssue(
                            code="FORBIDDEN_PROPERTY",
                            path=f"{req_path}/type",
                            message="request 不应包含 type",
                        )
                    )
                if "params" in req:
                    issues.append(
                        ValidationIssue(
                            code="FORBIDDEN_PROPERTY",
                            path=f"{req_path}/params",
                            message="request 不应重复包含 params",
                        )
                    )

                module_id = req.get("moduleId")
                sql_code = req.get("sqlCode")
                if not module_id:
                    issues.append(
                        ValidationIssue(
                            code="MISSING_MODULE_ID",
                            path=f"{req_path}/moduleId",
                            message="request 缺少 moduleId",
                        )
                    )
                if not sql_code:
                    issues.append(
                        ValidationIssue(
                            code="MISSING_SQL_CODE",
                            path=f"{req_path}/sqlCode",
                            message="request 缺少 sqlCode",
                        )
                    )

                if opts_catalog and module_id and sql_code:
                    modules_map = opts_catalog.get("modules", {})
                    mod_binding = modules_map.get(module_id)
                    if not mod_binding:
                        issues.append(
                            ValidationIssue(
                                code="CATALOG_BINDING_NOT_FOUND",
                                path=f"{req_path}/moduleId",
                                message=f"catalog 中不存在 request.moduleId: {module_id}",
                            )
                        )
                    else:
                        if mod_binding.get("sqlCode") != sql_code:
                            issues.append(
                                ValidationIssue(
                                    code="SQL_CODE_MISMATCH",
                                    path=f"{req_path}/sqlCode",
                                    message=f"request.sqlCode 与 catalog 模块 {module_id} 不一致",
                                )
                            )
                        submodule_id = req.get("submoduleId")
                        submodule_ids = mod_binding.get("submoduleIds")
                        if (
                            submodule_id
                            and isinstance(submodule_ids, list)
                            and submodule_id not in submodule_ids
                        ):
                            issues.append(
                                ValidationIssue(
                                    code="SUBMODULE_NOT_BOUND",
                                    path=f"{req_path}/submoduleId",
                                    message=f"submoduleId {submodule_id} 未绑定到 catalog 父模块 {module_id}",
                                )
                            )

        # Transform validation
        transform_source = ""
        transform_obj = dsl.get("transform")
        tf_path = f"{path_prefix}/transform/function"

        if not isinstance(transform_obj, dict):
            issues.append(
                ValidationIssue(
                    code="MISSING_TRANSFORM",
                    path=f"{path_prefix}/transform",
                    message="DSL 必须包含 transform",
                )
            )
        else:
            if transform_obj.get("language") != "javascript":
                issues.append(
                    ValidationIssue(
                        code="INVALID_LANGUAGE",
                        path=f"{path_prefix}/transform/language",
                        message="transform.language 必须为 javascript",
                    )
                )
            transform_source = str(transform_obj.get("function") or "").strip()

            if not re.search(r"^\s*function\s+transform\s*\(\s*responses\s*\)", transform_source):
                issues.append(
                    ValidationIssue(
                        code="INVALID_FUNCTION_SIGNATURE",
                        path=tf_path,
                        message="transform.function 必须使用 function transform(responses) 签名",
                    )
                )
            if not re.search(r"\breturn\b", transform_source):
                issues.append(
                    ValidationIssue(
                        code="MISSING_RETURN",
                        path=tf_path,
                        message="transform.function 必须包含 return 语句",
                    )
                )
            if "?." in transform_source:
                issues.append(
                    ValidationIssue(
                        code="FORBIDDEN_SYNTAX",
                        path=tf_path,
                        message="transform.function 不支持可选链语法 ?.",
                    )
                )
            if "??" in transform_source:
                issues.append(
                    ValidationIssue(
                        code="FORBIDDEN_SYNTAX",
                        path=tf_path,
                        message="transform.function 不支持空值合并语法 ??",
                    )
                )
            if re.search(r"\.toFixed\s*\(", transform_source):
                issues.append(
                    ValidationIssue(
                        code="FORBIDDEN_SYNTAX",
                        path=tf_path,
                        message="transform.function 不得使用 toFixed；展示格式化必须由 view.format 完成",
                    )
                )

            ast_issues = check_js_ast(transform_source, tf_path)
            issues.extend(ast_issues)

            for request_id in request_ids:
                escaped_id = escape_reg_exp(request_id)
                ref_pat = re.compile(
                    rf"responses\s*(?:\.\s*{escaped_id}\b|\[\s*['\"]{escaped_id}['\"]\s*\])"
                )
                if not ref_pat.search(transform_source):
                    issues.append(
                        ValidationIssue(
                            code="MISSING_REQUEST_REFERENCE",
                            path=tf_path,
                            message=f"transform.function 未引用 request：{request_id}",
                        )
                    )

        # View validation
        view_obj = dsl.get("view")
        view_fields: List[str] = []

        if not isinstance(view_obj, dict):
            issues.append(
                ValidationIssue(
                    code="MISSING_VIEW",
                    path=f"{path_prefix}/view",
                    message="DSL 必须包含 view",
                )
            )
        else:
            view_type = view_obj.get("type")
            if view_type not in ["table", "echarts"]:
                issues.append(
                    ValidationIssue(
                        code="INVALID_VIEW_TYPE",
                        path=f"{path_prefix}/view/type",
                        message="DSL 必须包含 table 或 echarts view",
                    )
                )
            elif view_type == "table":
                columns = view_obj.get("columns")
                if not isinstance(columns, list) or len(columns) == 0:
                    issues.append(
                        ValidationIssue(
                            code="MISSING_COLUMNS",
                            path=f"{path_prefix}/view/columns",
                            message="table view 必须包含 columns",
                        )
                    )
                else:
                    col_fields: Set[str] = set()
                    for c_idx, col in enumerate(columns):
                        col_path = f"{path_prefix}/view/columns[{c_idx}]"
                        if not isinstance(col, dict) or not col.get("field"):
                            issues.append(
                                ValidationIssue(
                                    code="MISSING_FIELD",
                                    path=f"{col_path}/field",
                                    message="column.field 必须是有效值",
                                )
                            )
                        else:
                            field_val = str(col["field"])
                            if field_val in col_fields:
                                issues.append(
                                    ValidationIssue(
                                        code="DUPLICATE_FIELD",
                                        path=f"{col_path}/field",
                                        message=f"table column.field 重复：{field_val}",
                                    )
                                )
                            col_fields.add(field_val)
                            view_fields.append(field_val)

                        if isinstance(col, dict) and col.get("format") is not None:
                            try:
                                field_name = col.get("field") if col.get("field") else c_idx
                                validate_format(col["format"], f"column {field_name}.format")
                            except Exception as err:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_FORMAT",
                                        path=f"{col_path}/format",
                                        message=str(err),
                                    )
                                )
            elif view_type == "echarts":
                if "xField" in view_obj:
                    issues.append(
                        ValidationIssue(
                            code="DEPRECATED_XFIELD",
                            path=f"{path_prefix}/view/xField",
                            message="echarts view 不再使用 xField，请使用 dataset.dimensions 与 series.encode",
                        )
                    )
                legend = view_obj.get("legend")
                if not isinstance(legend, dict):
                    issues.append(
                        ValidationIssue(
                            code="MISSING_LEGEND",
                            path=f"{path_prefix}/view/legend",
                            message="echarts view 必须包含 legend",
                        )
                    )
                else:
                    if legend.get("show") is not True:
                        issues.append(
                            ValidationIssue(
                                code="INVALID_LEGEND",
                                path=f"{path_prefix}/view/legend/show",
                                message="echarts legend.show 必须为 true",
                            )
                        )
                    legend_data = legend.get("data")
                    if not isinstance(legend_data, list) or len(legend_data) == 0:
                        issues.append(
                            ValidationIssue(
                                code="MISSING_LEGEND_DATA",
                                path=f"{path_prefix}/view/legend/data",
                                message="echarts legend.data 必须是非空数组",
                            )
                        )

                dimension_set: Set[str] = set()
                dataset = view_obj.get("dataset")
                if not isinstance(dataset, dict):
                    issues.append(
                        ValidationIssue(
                            code="MISSING_DATASET",
                            path=f"{path_prefix}/view/dataset",
                            message="echarts view 必须包含 dataset",
                        )
                    )
                else:
                    if dataset.get("source") != "$transform":
                        issues.append(
                            ValidationIssue(
                                code="INVALID_DATASET_SOURCE",
                                path=f"{path_prefix}/view/dataset/source",
                                message='echarts dataset.source 必须为 "$transform"',
                            )
                        )
                    dimensions = dataset.get("dimensions")
                    if not isinstance(dimensions, list) or len(dimensions) == 0:
                        issues.append(
                            ValidationIssue(
                                code="MISSING_DIMENSIONS",
                                path=f"{path_prefix}/view/dataset/dimensions",
                                message="echarts dataset.dimensions 必须是非空数组",
                            )
                        )
                    else:
                        view_fields = [str(d) for d in dimensions]
                        dimension_set = {str(d) for d in dimensions}

                series_list = view_obj.get("series")
                if not isinstance(series_list, list) or len(series_list) == 0:
                    issues.append(
                        ValidationIssue(
                            code="MISSING_SERIES",
                            path=f"{path_prefix}/view/series",
                            message="echarts view 必须包含 series",
                        )
                    )
                else:
                    legend_names: List[str] = []
                    x_fields: Set[str] = set()
                    cartesian_series_count = 0

                    for s_idx, series in enumerate(series_list):
                        s_path = f"{path_prefix}/view/series[{s_idx}]"
                        if not isinstance(series, dict):
                            issues.append(
                                ValidationIssue(
                                    code="INVALID_SERIES",
                                    path=s_path,
                                    message="series 必须是对象",
                                )
                            )
                            continue
                        if "chartType" in series:
                            issues.append(
                                ValidationIssue(
                                    code="DEPRECATED_CHART_TYPE",
                                    path=f"{s_path}/chartType",
                                    message="echarts series 不再使用 chartType，请使用 type",
                                )
                            )
                        series_name = series.get("name")
                        if not series_name:
                            issues.append(
                                ValidationIssue(
                                    code="MISSING_SERIES_NAME",
                                    path=f"{s_path}/name",
                                    message=f"series[{s_idx}].name 必须是有效值",
                                )
                            )
                        else:
                            legend_names.append(str(series_name))

                        series_type = series.get("type")
                        if series_type not in ["line", "bar", "pie"]:
                            issues.append(
                                ValidationIssue(
                                    code="INVALID_SERIES_TYPE",
                                    path=f"{s_path}/type",
                                    message=f"不支持的 series.type: {series_type}",
                                )
                            )

                        encode = series.get("encode")
                        if not isinstance(encode, dict):
                            issues.append(
                                ValidationIssue(
                                    code="MISSING_ENCODE",
                                    path=f"{s_path}/encode",
                                    message="series 必须包含 encode",
                                )
                            )
                        elif series_type == "pie":
                            item_name = encode.get("itemName")
                            if not item_name or item_name not in dimension_set:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_ENCODE_ITEM_NAME",
                                        path=f"{s_path}/encode/itemName",
                                        message=f"series {series_name}.encode.itemName 必须引用 dataset.dimensions 中的字段",
                                    )
                                )
                            val = encode.get("value")
                            if not val or val not in dimension_set:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_ENCODE_VALUE",
                                        path=f"{s_path}/encode/value",
                                        message=f"series {series_name}.encode.value 必须引用 dataset.dimensions 中的字段",
                                    )
                                )
                        else:
                            cartesian_series_count += 1
                            y_axis_idx = series.get("yAxisIndex")
                            if y_axis_idx is not None:
                                if type(y_axis_idx) is not int or y_axis_idx < 0 or y_axis_idx > 1:
                                    issues.append(
                                        ValidationIssue(
                                            code="INVALID_Y_AXIS_INDEX",
                                            path=f"{s_path}/yAxisIndex",
                                            message="yAxisIndex 只能为 0 或 1",
                                        )
                                    )
                            encode_x = encode.get("x")
                            if not encode_x or encode_x not in dimension_set:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_ENCODE_X",
                                        path=f"{s_path}/encode/x",
                                        message=f"series {series_name}.encode.x 必须引用 dataset.dimensions 中的字段",
                                    )
                                )
                            else:
                                x_fields.add(str(encode_x))

                            encode_y = encode.get("y")
                            if not encode_y or encode_y not in dimension_set:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_ENCODE_Y",
                                        path=f"{s_path}/encode/y",
                                        message=f"series {series_name}.encode.y 必须引用 dataset.dimensions 中的字段",
                                    )
                                )

                        if series.get("format") is not None:
                            try:
                                format_label = f"series {series_name or s_idx}.format"
                                validate_format(series["format"], format_label)
                            except Exception as err:
                                issues.append(
                                    ValidationIssue(
                                        code="INVALID_FORMAT",
                                        path=f"{s_path}/format",
                                        message=str(err),
                                    )
                                )

                    # Legend order check
                    if isinstance(legend, dict) and isinstance(legend.get("data"), list):
                        if legend.get("data") != legend_names:
                            issues.append(
                                ValidationIssue(
                                    code="LEGEND_SERIES_MISMATCH",
                                    path=f"{path_prefix}/view/legend/data",
                                    message="echarts legend.data 必须与 series.name 顺序一致",
                                )
                            )

                    if len(x_fields) > 1:
                        issues.append(
                            ValidationIssue(
                                code="CARTESIAN_X_MISMATCH",
                                path=f"{path_prefix}/view/series",
                                message="同一 ECharts 图表的非饼图 series 必须使用相同 encode.x",
                            )
                        )

                    if cartesian_series_count > 0:
                        x_axis = view_obj.get("xAxis")
                        if not isinstance(x_axis, dict):
                            issues.append(
                                ValidationIssue(
                                    code="MISSING_X_AXIS",
                                    path=f"{path_prefix}/view/xAxis",
                                    message="包含 line/bar 的 echarts view 必须包含 xAxis 对象",
                                )
                            )
                        y_axis = view_obj.get("yAxis")
                        if not isinstance(y_axis, list) or len(y_axis) == 0:
                            issues.append(
                                ValidationIssue(
                                    code="MISSING_Y_AXIS",
                                    path=f"{path_prefix}/view/yAxis",
                                    message="包含 line/bar 的 echarts view 必须包含非空 yAxis 数组",
                                )
                            )
                        elif isinstance(series_list, list):
                            for series in series_list:
                                if isinstance(series, dict) and series.get("type") != "pie":
                                    idx = (
                                        0
                                        if series.get("yAxisIndex") is None
                                        else series.get("yAxisIndex")
                                    )
                                    if (
                                        isinstance(y_axis, list)
                                        and isinstance(idx, int)
                                        and idx >= len(y_axis)
                                    ):
                                        issues.append(
                                            ValidationIssue(
                                                code="Y_AXIS_INDEX_OUT_OF_BOUNDS",
                                                path=f"{path_prefix}/view/series",
                                                message=f"series {series.get('name')}.yAxisIndex 引用了不存在的 Y 轴",
                                            )
                                        )

        # Source writes field check
        if transform_source and len(view_fields) > 0:
            for field in view_fields:
                if not source_writes_field(transform_source, field):
                    issues.append(
                        ValidationIssue(
                            code="MISSING_FIELD_WRITE",
                            path=f"{path_prefix}/transform/function",
                            message=f"transform.function 未生成 view 字段：{field}",
                        )
                    )

    if len(issues) > 0:
        return ValidationFailure(ok=False, errors=issues)

    return ValidationSuccess(ok=True, dsls=dsls_success)


# Aliases for JS camelCase compatibility
validateVmReportDslSet = validate_vm_report_dsl_set
