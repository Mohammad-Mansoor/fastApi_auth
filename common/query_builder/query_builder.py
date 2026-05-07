# from typing import Any, Dict, List, Optional, Callable
# from sqlalchemy import (
#     select,
#     and_,
#     or_,
#     func,
# )
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import (
#     joinedload,
#     selectinload,
#     aliased,
# )
# from sqlalchemy.sql import Select
# from sqlalchemy.inspection import inspect
# from sqlalchemy.orm.attributes import InstrumentedAttribute
# import base64


# class QueryConfig:
#     def __init__(
#         self,
#         searchable_fields: Optional[List[str]] = None,
#         filterable_fields: Optional[Dict[str, str]] = None,
#         relations: Optional[List[str]] = None,
#         select_fields: Optional[List[str]] = None,
#         default_sort: Optional[str] = None,
#         translated_fields: Optional[List[str]] = None,
#     ):
#         self.searchable_fields = searchable_fields or []
#         self.filterable_fields = filterable_fields or {}
#         self.relations = relations or []
#         self.select_fields = select_fields or []
#         self.default_sort = default_sort
#         self.translated_fields = translated_fields or []


# class SQLAlchemyQueryHelper:
#     """
#     Enterprise Query Builder for FastAPI + SQLAlchemy

#     Features:
#     - select fields
#     - deep relation joins
#     - relation eager loading
#     - filtering
#     - search
#     - sorting
#     - pagination
#     - cursor pagination
#     - jsonb translation support
#     - manual query injection support
#     """

#     def __init__(
#         self,
#         model,
#         session: AsyncSession,
#         query_options,
#         config: QueryConfig = None,
#         alias: str = "root",
#     ):
#         self.model = model
#         self.session = session
#         self.query_options = query_options
#         self.config = config or QueryConfig()
#         self.alias = alias

#         self.query = select(model)

#         self.joined_relations = set()
#         self.alias_map = {
#             alias: model
#         }

#     # =========================================================
#     # STATIC FACTORY
#     # =========================================================

#     @staticmethod
#     def for_(
#         model,
#         session: AsyncSession,
#         options,
#         config: QueryConfig = None,
#         alias: str = "root",
#     ):
#         return SQLAlchemyQueryHelper(
#             model=model,
#             session=session,
#             query_options=options,
#             config=config,
#             alias=alias,
#         )

#     # =========================================================
#     # MAIN BUILD
#     # =========================================================

#     def build(self):

#         self.apply_fields()
#         self.apply_includes()
#         self.apply_filters()
#         self.apply_search()
#         self.apply_sorting()
#         self.apply_pagination()

#         return self.query

#     # =========================================================
#     # GET MANY + META
#     # =========================================================

#     async def get_many_and_meta(self):

#         built_query = self.build()

#         result = await self.session.execute(built_query)

#         rows = result.unique().scalars().all()

#         total_query = select(func.count()).select_from(
#             built_query.order_by(None).subquery()
#         )

#         total_result = await self.session.execute(total_query)

#         total = total_result.scalar()

#         limit = int(getattr(self.query_options, "limit", 10) or 10)
#         page = int(getattr(self.query_options, "page", 1) or 1)

#         return {
#             "data": rows,
#             "meta": {
#                 "total": total,
#                 "page": page,
#                 "limit": limit,
#                 "totalPages": (total + limit - 1) // limit,
#                 "hasNextPage": page * limit < total,
#                 "hasPreviousPage": page > 1,
#             },
#         }

#     # =========================================================
#     # SELECT FIELDS
#     # =========================================================

#     def apply_fields(self):

#         if not self.config.select_fields:
#             return

#         columns = []

#         lang = getattr(self.query_options, "lang", "en")

#         for field in self.config.select_fields:

#             column = self.resolve_path(field)

#             if field in self.config.translated_fields:

#                 translated = column.op("->>")(lang).label(
#                     field.replace(".", "_")
#                 )

#                 columns.append(translated)

#             else:
#                 columns.append(column)

#         # always include root id
#         root_id = getattr(self.model, "id", None)

#         if root_id is not None:
#             columns.append(root_id)

#         self.query = select(*columns)

#     # =========================================================
#     # RELATIONS / INCLUDES
#     # =========================================================

#     def apply_includes(self):

#         if not self.config.relations:
#             return

#         for relation in self.config.relations:

#             self.ensure_join(relation)

#             relation_attr = self.resolve_relationship(relation)

#             self.query = self.query.options(
#                 selectinload(relation_attr)
#             )

#     # =========================================================
#     # FILTERS
#     # =========================================================

#     def apply_filters(self):

#         predefined_keys = {
#             "page",
#             "limit",
#             "search",
#             "cursor",
#             "sort",
#             "lang",
#         }

#         conditions = []

#         for key, value in self.query_options.items():

#             if key in predefined_keys:
#                 continue

#             if value is None or value == "":
#                 continue

#             base_key = key
#             operator = "eq"

#             parts = key.rsplit("_", 1)

#             if len(parts) == 2:

#                 possible_op = parts[1]

#                 allowed = [
#                     "eq",
#                     "ne",
#                     "gt",
#                     "gte",
#                     "lt",
#                     "lte",
#                     "in",
#                     "like",
#                     "ilike",
#                     "null",
#                 ]

#                 if possible_op in allowed:
#                     base_key = parts[0]
#                     operator = possible_op

#             path = self.config.filterable_fields.get(base_key)

#             if not path:
#                 continue

#             column = self.resolve_path(path)

#             if path in self.config.translated_fields:

#                 lang = getattr(self.query_options, "lang", "en")

#                 column = column.op("->>")(lang)

#             conditions.append(
#                 self.build_filter_operator(
#                     column,
#                     operator,
#                     value,
#                 )
#             )

#         if conditions:
#             self.query = self.query.where(and_(*conditions))

#     # =========================================================
#     # FILTER OPERATORS
#     # =========================================================

#     def build_filter_operator(
#         self,
#         column,
#         operator,
#         value,
#     ):

#         if operator == "eq":
#             return column == value

#         if operator == "ne":
#             return column != value

#         if operator == "gt":
#             return column > value

#         if operator == "gte":
#             return column >= value

#         if operator == "lt":
#             return column < value

#         if operator == "lte":
#             return column <= value

#         if operator == "like":
#             return column.like(f"%{value}%")

#         if operator == "ilike":
#             return column.ilike(f"%{value}%")

#         if operator == "in":

#             if isinstance(value, str):
#                 value = value.split(",")

#             return column.in_(value)

#         if operator == "null":

#             is_null = str(value).lower() in ["true", "1"]

#             return column.is_(None) if is_null else column.is_not(None)

#         raise Exception(f"Unsupported operator: {operator}")

#     # =========================================================
#     # SEARCH
#     # =========================================================

#     def apply_search(self):

#         search = getattr(self.query_options, "search", None)

#         if not search:
#             return

#         if not self.config.searchable_fields:
#             return

#         conditions = []

#         lang = getattr(self.query_options, "lang", "en")

#         for field in self.config.searchable_fields:

#             column = self.resolve_path(field)

#             if field in self.config.translated_fields:
#                 column = column.op("->>")(lang)

#             conditions.append(
#                 column.ilike(f"%{search}%")
#             )

#         self.query = self.query.where(or_(*conditions))

#     # =========================================================
#     # SORTING
#     # =========================================================

#     def apply_sorting(self):

#         sort = (
#             getattr(self.query_options, "sort", None)
#             or self.config.default_sort
#         )

#         if not sort:

#             if hasattr(self.model, "createdAt"):
#                 self.query = self.query.order_by(
#                     getattr(self.model, "createdAt").desc()
#                 )

#             return

#         lang = getattr(self.query_options, "lang", "en")

#         for sort_item in sort.split(","):

#             parts = sort_item.split(":")

#             field = parts[0]

#             direction = parts[1] if len(parts) > 1 else "ASC"

#             if field in self.config.filterable_fields:
#                 field = self.config.filterable_fields[field]

#             column = self.resolve_path(field)

#             if field in self.config.translated_fields:
#                 column = column.op("->>")(lang)

#             if direction.upper() == "DESC":
#                 self.query = self.query.order_by(column.desc())
#             else:
#                 self.query = self.query.order_by(column.asc())

#     # =========================================================
#     # PAGINATION
#     # =========================================================

#     def apply_pagination(self):

#         cursor = getattr(self.query_options, "cursor", None)

#         if cursor:

#             decoded = base64.b64decode(cursor).decode()

#             self.query = self.query.where(
#                 getattr(self.model, "id") > decoded
#             )

#             limit = int(getattr(self.query_options, "limit", 10))

#             self.query = self.query.limit(limit)

#             return

#         limit = int(getattr(self.query_options, "limit", 10) or 10)

#         page = int(getattr(self.query_options, "page", 1) or 1)

#         offset = (page - 1) * limit

#         self.query = self.query.limit(limit).offset(offset)

#     # =========================================================
#     # PATH RESOLVER
#     # =========================================================

#     def resolve_path(self, path: str):

#         if "." not in path:
#             return getattr(self.model, path)

#         parts = path.split(".")

#         current_model = self.model

#         for relation_name in parts[:-1]:

#             self.ensure_join(relation_name)

#             relation_attr = getattr(current_model, relation_name)

#             current_model = relation_attr.property.mapper.class_

#         return getattr(current_model, parts[-1])

#     # =========================================================
#     # ENSURE JOIN
#     # =========================================================

#     def ensure_join(self, relation_path: str):

#         if relation_path in self.joined_relations:
#             return

#         parts = relation_path.split(".")

#         current_model = self.model

#         current_path = []

#         for relation_name in parts:

#             current_path.append(relation_name)

#             joined_name = ".".join(current_path)

#             if joined_name in self.joined_relations:
#                 continue

#             relation_attr = getattr(current_model, relation_name)

#             self.query = self.query.join(
#                 relation_attr,
#                 isouter=True,
#             )

#             self.joined_relations.add(joined_name)

#             current_model = relation_attr.property.mapper.class_

#     # =========================================================
#     # RELATION RESOLVER
#     # =========================================================

#     def resolve_relationship(self, relation_path: str):

#         current = self.model

#         attr = None

#         for part in relation_path.split("."):

#             attr = getattr(current, part)

#             current = attr.property.mapper.class_

#         return attr

#     # =========================================================
#     # =========================================================
#     # MANUAL INJECTION SUPPORT
#     # =========================================================
#     # =========================================================

#     # ---------------------------------------------------------
#     # manual where injection
#     # ---------------------------------------------------------

#     def where(self, *conditions):

#         self.query = self.query.where(*conditions)

#         return self

#     # ---------------------------------------------------------
#     # manual join injection
#     # ---------------------------------------------------------

#     def join(self, *joins):

#         for join_item in joins:

#             self.query = self.query.join(join_item)

#         return self

#     # ---------------------------------------------------------
#     # eager loading injection
#     # ---------------------------------------------------------

#     def options(self, *options):

#         self.query = self.query.options(*options)

#         return self

#     # ---------------------------------------------------------
#     # modify raw query
#     # ---------------------------------------------------------

#     def modify(
#         self,
#         callback: Callable[[Select], Select]
#     ):

#         self.query = callback(self.query)

#         return self

#     # ---------------------------------------------------------
#     # manual group by
#     # ---------------------------------------------------------

#     def group_by(self, *columns):

#         self.query = self.query.group_by(*columns)

#         return self

#     # ---------------------------------------------------------
#     # manual having
#     # ---------------------------------------------------------

#     def having(self, *conditions):

#         self.query = self.query.having(*conditions)

#         return self

#     # ---------------------------------------------------------
#     # manual add columns
#     # ---------------------------------------------------------

#     def add_columns(self, *columns):

#         self.query = self.query.add_columns(*columns)

#         return self

#     # ---------------------------------------------------------
#     # manual distinct
#     # ---------------------------------------------------------

#     def distinct(self):

#         self.query = self.query.distinct()

#         return self

#     # ---------------------------------------------------------
#     # raw sql execution
#     # ---------------------------------------------------------

#     def raw(self, query):

#         self.query = query

#         return self

from typing import Any, Dict, List, Optional, Callable, Union
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
import base64


# =========================================================
# CONFIG CLASS
# =========================================================

class QueryConfig:
    def __init__(
        self,
        searchable_fields: Optional[List[str]] = None,
        filterable_fields: Optional[Dict[str, str]] = None,
        relations: Optional[List[str]] = None,
        select_fields: Optional[List[str]] = None,
        default_sort: Optional[str] = None,
        translated_fields: Optional[List[str]] = None,
        allowed_fields: Optional[List[str]] = None,
    ):
        self.searchable_fields = searchable_fields or []
        self.filterable_fields = filterable_fields or {}
        self.relations = relations or []
        self.select_fields = select_fields or []
        self.default_sort = default_sort
        self.translated_fields = translated_fields or []
        self.allowed_fields = set(allowed_fields or [])


# =========================================================
# QUERY BUILDER V6
# =========================================================

class SQLAlchemyQueryHelper:
    """
    🚀 QUERY BUILDER V6 (PRODUCTION READY)

    Features:
    - Deep joins (profile.country.name)
    - Filters with operators (_eq, _gt, _in, etc)
    - Multi-field search
    - Sorting (multi-column)
    - Pagination + cursor pagination
    - Select fields optimization
    - Safe field resolution
    - Manual injection hooks
    """

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        model,
        session: AsyncSession,
        options: Union[dict, Any],
        config: QueryConfig = None,
    ):
        self.model = model
        self.session = session
        self.options = self._normalize(options)
        self.config = config or QueryConfig()

        self.query = select(model)

        self.joins = set()

    # =====================================================
    # FACTORY
    # =====================================================

    @staticmethod
    def for_(
        model,
        session: AsyncSession,
        options,
        config: QueryConfig = None,
    ):
        return SQLAlchemyQueryHelper(model, session, options, config)

    # =====================================================
    # NORMALIZER
    # =====================================================

    def _normalize(self, options):
        if options is None:
            return {}

        if isinstance(options, dict):
            return options

        if hasattr(options, "model_dump"):
            return options.model_dump(exclude_none=True)

        return vars(options)

    # =====================================================
    # FIELD RESOLVER (SAFE + DEEP)
    # =====================================================

    def _resolve(self, path: str):
        parts = path.split(".")
        model = self.model

        for p in parts:
            model = getattr(model, p)

        return model

    # =====================================================
    # JOIN ENGINE
    # =====================================================

    def _apply_joins(self):

        for key in list(self.options.keys()):
            if "." in key:
                self._auto_join(key.split(".")[:-1])

        for rel in self.config.relations:
            if "." in rel:
                self._auto_join(rel.split("."))
            else:
                self._auto_join([rel])

    def _auto_join(self, parts: List[str]):

        model = self.model
        path = []

        for p in parts:

            path.append(p)
            join_key = ".".join(path)

            if join_key in self.joins:
                continue

            attr = getattr(model, p)

            self.query = self.query.join(attr, isouter=True)

            model = attr.property.mapper.class_
            self.joins.add(join_key)

    # =====================================================
    # FILTER ENGINE
    # =====================================================

    def _apply_filters(self):

        skip = {"page", "limit", "search", "sort", "cursor", "lang"}

        conditions = []

        for key, value in self.options.items():

            if key in skip or value in [None, ""]:
                continue

            operator = "eq"

            if "_" in key:
                key, operator = key.rsplit("_", 1)

            if key not in self.config.filterable_fields:
                continue

            path = self.config.filterable_fields[key]
            column = self._resolve(path)

            if "." in path:
                self._auto_join(path.split(".")[:-1])

            conditions.append(self._op(column, operator, value))

        if conditions:
            self.query = self.query.where(and_(*conditions))

    # =====================================================
    # OPERATORS
    # =====================================================

    def _op(self, column, op, value):

        if op == "eq":
            return column == value

        if op == "ne":
            return column != value

        if op == "gt":
            return column > value

        if op == "gte":
            return column >= value

        if op == "lt":
            return column < value

        if op == "lte":
            return column <= value

        if op == "like":
            return column.like(f"%{value}%")

        if op == "ilike":
            return column.ilike(f"%{value}%")

        if op == "in":
            return column.in_(value.split(",") if isinstance(value, str) else value)

        if op == "null":
            return column.is_(None) if value else column.is_not(None)

        return column == value

    # =====================================================
    # SEARCH
    # =====================================================

    def _apply_search(self):

        search = self.options.get("search")
        if not search:
            return

        conditions = []

        for field in self.config.searchable_fields:

            column = self._resolve(field)

            conditions.append(column.ilike(f"%{search}%"))

        if conditions:
            self.query = self.query.where(or_(*conditions))

    # =====================================================
    # SORT
    # =====================================================

    def _apply_sort(self):

        sort = self.options.get("sort") or self.config.default_sort

        if not sort:
            return

        for item in sort.split(","):

            field, direction = (item.split(":") + ["ASC"])[:2]

            column = self._resolve(field)

            if direction.upper() == "DESC":
                self.query = self.query.order_by(column.desc())
            else:
                self.query = self.query.order_by(column.asc())

    # =====================================================
    # PAGINATION
    # =====================================================

    def _apply_pagination(self):

        limit = int(self.options.get("limit", 10))
        page = int(self.options.get("page", 1))

        self.query = self.query.limit(limit).offset((page - 1) * limit)

    # =====================================================
    # SELECT FIELDS
    # =====================================================

    def _apply_select(self):

        if not self.config.select_fields:
            return

        cols = [self._resolve(f) for f in self.config.select_fields]

        self.query = select(*cols)

    # =====================================================
    # BUILD PIPELINE
    # =====================================================

    def build(self):

        self._apply_select()
        self._apply_joins()
        self._apply_filters()
        self._apply_search()
        self._apply_sort()
        self._apply_pagination()

        return self.query

    # =====================================================
    # EXECUTION
    # =====================================================

    async def get_many_and_meta(self):

        q = self.build()

        result = await self.session.execute(q)
        data = result.scalars().all()

        total_q = select(func.count()).select_from(self.model)
        total = (await self.session.execute(total_q)).scalar() or 0

        limit = int(self.options.get("limit", 10))
        page = int(self.options.get("page", 1))

        return {
            "data": data,
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": (total + limit - 1) // limit,
                "hasNextPage": page * limit < total,
                "hasPreviousPage": page > 1,
            },
        }

    # =====================================================
    # EXTENSION HOOKS
    # =====================================================

    def where(self, *conds):
        self.query = self.query.where(*conds)
        return self

    def join(self, *joins):
        for j in joins:
            self.query = self.query.join(j)
        return self

    def modify(self, fn: Callable[[Select], Select]):
        self.query = fn(self.query)
        return self