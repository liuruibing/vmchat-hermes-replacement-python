// 由 Hermes vm-report-dsl/references/dsl.schema.json 自动生成。
// 请运行 npm run sync:vmchat-contracts 更新，禁止手工修改。
export default {
  "$schema": "http://json-schema.org/draft-07/schema",
  "$id": "https://local.hermes/vm-report-dsl.schema.json",
  "title": "VM Report DSL response",
  "oneOf": [
    {
      "$ref": "#/definitions/dsl"
    },
    {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/dsl"
      }
    }
  ],
  "definitions": {
    "nonEmptyString": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!\\{[^{}]+\\}$).+"
    },
    "uuid": {
      "type": "string",
      "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
    },
    "format": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type"
      ],
      "properties": {
        "type": {
          "enum": [
            "raw",
            "text",
            "date",
            "decimal",
            "percentage"
          ]
        },
        "digits": {
          "type": "integer",
          "minimum": 0
        },
        "prefix": {
          "type": "string"
        },
        "suffix": {
          "type": "string"
        },
        "nullValue": {
          "type": "string"
        }
      }
    },
    "request": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "moduleId",
        "sqlCode"
      ],
      "properties": {
        "id": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "moduleId": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9]*$"
        },
        "submoduleId": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9]*$"
        },
        "sqlCode": {
          "$ref": "#/definitions/uuid"
        }
      }
    },
    "transform": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "language",
        "function"
      ],
      "properties": {
        "language": {
          "const": "javascript"
        },
        "function": {
          "$ref": "#/definitions/nonEmptyString"
        }
      }
    },
    "column": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "field",
        "label"
      ],
      "properties": {
        "field": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "label": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "unit": {
          "type": "string"
        },
        "format": {
          "$ref": "#/definitions/format"
        }
      }
    },
    "tableView": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "title",
        "columns"
      ],
      "properties": {
        "type": {
          "const": "table"
        },
        "title": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "columns": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/column"
          }
        }
      }
    },
    "axis": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type"
      ],
      "properties": {
        "type": {
          "enum": [
            "category",
            "value",
            "time",
            "log"
          ]
        },
        "name": {
          "type": "string"
        }
      }
    },
    "cartesianSeries": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "name",
        "encode",
        "format"
      ],
      "properties": {
        "type": {
          "enum": [
            "line",
            "bar"
          ]
        },
        "name": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "encode": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "x",
            "y"
          ],
          "properties": {
            "x": {
              "$ref": "#/definitions/nonEmptyString"
            },
            "y": {
              "$ref": "#/definitions/nonEmptyString"
            }
          }
        },
        "yAxisIndex": {
          "type": "integer",
          "minimum": 0,
          "maximum": 1
        },
        "stack": {
          "type": "string"
        },
        "format": {
          "$ref": "#/definitions/format"
        }
      }
    },
    "pieSeries": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "name",
        "encode",
        "format"
      ],
      "properties": {
        "type": {
          "const": "pie"
        },
        "name": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "encode": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "itemName",
            "value"
          ],
          "properties": {
            "itemName": {
              "$ref": "#/definitions/nonEmptyString"
            },
            "value": {
              "$ref": "#/definitions/nonEmptyString"
            }
          }
        },
        "format": {
          "$ref": "#/definitions/format"
        }
      }
    },
    "echartsView": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "title",
        "legend",
        "dataset",
        "series"
      ],
      "properties": {
        "type": {
          "const": "echarts"
        },
        "title": {
          "$ref": "#/definitions/nonEmptyString"
        },
        "legend": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "show",
            "data"
          ],
          "properties": {
            "show": {
              "const": true
            },
            "data": {
              "type": "array",
              "minItems": 1,
              "items": {
                "$ref": "#/definitions/nonEmptyString"
              },
              "uniqueItems": true
            }
          }
        },
        "dataset": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "source",
            "dimensions"
          ],
          "properties": {
            "source": {
              "const": "$transform"
            },
            "dimensions": {
              "type": "array",
              "minItems": 1,
              "items": {
                "$ref": "#/definitions/nonEmptyString"
              },
              "uniqueItems": true
            }
          }
        },
        "xAxis": {
          "$ref": "#/definitions/axis"
        },
        "yAxis": {
          "type": "array",
          "minItems": 1,
          "maxItems": 2,
          "items": {
            "$ref": "#/definitions/axis"
          }
        },
        "series": {
          "type": "array",
          "minItems": 1,
          "items": {
            "oneOf": [
              {
                "$ref": "#/definitions/cartesianSeries"
              },
              {
                "$ref": "#/definitions/pieSeries"
              }
            ]
          }
        }
      }
    },
    "dsl": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "action",
        "id",
        "requests",
        "transform",
        "view"
      ],
      "properties": {
        "action": {
          "enum": [
            "create",
            "update"
          ]
        },
        "id": {
          "$ref": "#/definitions/uuid"
        },
        "requests": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/request"
          }
        },
        "transform": {
          "$ref": "#/definitions/transform"
        },
        "view": {
          "oneOf": [
            {
              "$ref": "#/definitions/tableView"
            },
            {
              "$ref": "#/definitions/echartsView"
            }
          ]
        }
      }
    }
  }
}
