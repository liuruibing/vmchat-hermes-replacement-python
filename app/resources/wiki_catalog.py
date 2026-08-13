from typing import Any, Dict, Optional
from app.resources.resource_types import LoadedResources


def get_wiki_tree(resources: LoadedResources) -> Dict[str, Any]:
    sorted_module_ids = sorted(resources.moduleMarkdownMap.keys())
    module_children = [
        {
            "type": "file",
            "name": f"{module_id}.md",
            "path": f"catalog/modules/{module_id}.md",
            "documentId": module_id,
        }
        for module_id in sorted_module_ids
    ]

    return {
        "catalogVersion": resources.manifest.catalogVersion,
        "tree": [
            {
                "type": "directory",
                "name": "catalog",
                "path": "catalog",
                "children": [
                    {
                        "type": "file",
                        "name": "index.md",
                        "path": "catalog/index.md",
                        "documentId": "index",
                    },
                    {
                        "type": "file",
                        "name": "metrics.md",
                        "path": "catalog/metrics.md",
                        "documentId": "metrics",
                    },
                    {
                        "type": "directory",
                        "name": "modules",
                        "path": "catalog/modules",
                        "children": module_children,
                    },
                ],
            }
        ],
    }


def get_wiki_document(resources: LoadedResources, document_id: str) -> Optional[Dict[str, Any]]:
    if document_id == "index":
        return {
            "documentId": "index",
            "path": "catalog/index.md",
            "markdown": resources.catalogIndexMd,
        }
    if document_id == "metrics":
        return {
            "documentId": "metrics",
            "path": "catalog/metrics.md",
            "markdown": resources.catalogMetricsMd,
        }
    if document_id in resources.moduleMarkdownMap:
        return {
            "documentId": document_id,
            "path": f"catalog/modules/{document_id}.md",
            "markdown": resources.moduleMarkdownMap[document_id],
        }
    return None
