# =========================================================
# IMPORTS
# =========================================================

# SQLAlchemy async database session
from sqlalchemy.ext.asyncio import AsyncSession

# FastAPI dependency injection
from fastapi import Depends

# Your database session provider
from core.database import get_db

# Your SQLAlchemy models
from modules.users.models import User

# Query helper engine
from core.query_engine import (
    SQLAlchemyQueryHelper,
    QueryConfig,
)

# DTO that contains query params from frontend
from core.dto.query_options import QueryOptionsDto

# SQLAlchemy functions for advanced querying
from sqlalchemy import or_, and_, func

# Optional eager loading optimization
from sqlalchemy.orm import selectinload

# =========================================================
# EXAMPLE FASTAPI CONTROLLER
# =========================================================

@router.get("/users")
async def get_users(
    # Automatically reads query params from URL
    # Example:
    # ?page=1&limit=10&search=mansoor
    query_options: QueryOptionsDto = Depends(),

    # Inject async database session
    db: AsyncSession = Depends(get_db),
):

    # =====================================================
    # CREATE QUERY BUILDER
    # =====================================================

    query = (
        SQLAlchemyQueryHelper.for_(

            # -------------------------------------------------
            # ROOT MODEL
            # -------------------------------------------------
            # Main table we are querying
            # Equivalent to:
            # SELECT * FROM users
            # -------------------------------------------------
            model=User,

            # -------------------------------------------------
            # DATABASE SESSION
            # -------------------------------------------------
            session=db,

            # -------------------------------------------------
            # QUERY PARAMS FROM FRONTEND
            # -------------------------------------------------
            # Contains:
            # page
            # limit
            # search
            # sort
            # filters
            # etc
            # -------------------------------------------------
            options=query_options,

            # -------------------------------------------------
            # QUERY CONFIGURATION
            # -------------------------------------------------
            config=QueryConfig(

                # =================================================
                # SEARCHABLE FIELDS
                # =================================================
                # These fields are searched when:
                #
                # ?search=mansoor
                #
                # SQL Generated:
                #
                # WHERE
                # firstName ILIKE '%mansoor%'
                # OR email ILIKE '%mansoor%'
                # OR profile.bio ILIKE '%mansoor%'
                #
                # =================================================
                searchable_fields=[
                    "firstName",
                    "email",
                    "profile.bio",
                ],

                # =================================================
                # FILTERABLE FIELDS
                # =================================================
                # Allows frontend filters safely
                #
                # Frontend:
                # ?status=active
                #
                # Maps to:
                # User.status
                #
                #
                # Frontend:
                # ?country=Afghanistan
                #
                # Maps to:
                # profile.country.name
                #
                # =================================================
                filterable_fields={

                    # frontend key -> database path
                    "status": "status",

                    # nested relation filtering
                    "country": "profile.country.name",

                    # simple relation
                    "role": "role.name",

                    # direct column
                    "isActive": "isActive",
                },

                # =================================================
                # RELATIONS TO LOAD
                # =================================================
                # Automatically joins relations
                #
                # Equivalent TypeORM:
                # leftJoinAndSelect(...)
                #
                # Prevents N+1 problems
                #
                # =================================================
                relations=[

                    # User.profile
                    "profile",

                    # User.profile.country
                    "profile.country",

                    # User.role
                    "role",
                ],

                # =================================================
                # SELECT ONLY SPECIFIC FIELDS
                # =================================================
                # Reduces payload size
                #
                # Equivalent SQL:
                #
                # SELECT
                #   id,
                #   firstName,
                #   email
                #
                # =================================================
                select_fields=[
                    "id",
                    "firstName",
                    "lastName",
                    "email",
                    "profile.bio",
                ],

                # =================================================
                # DEFAULT SORT
                # =================================================
                # Used when frontend does NOT send:
                #
                # ?sort=
                #
                # =================================================
                default_sort="createdAt:DESC",

                # =================================================
                # TRANSLATED JSONB FIELDS
                # =================================================
                # PostgreSQL JSONB multilingual fields
                #
                # Example DB:
                #
                # name = {
                #   "en": "Afghanistan",
                #   "dr": "افغانستان"
                # }
                #
                # Automatically extracts:
                #
                # name->>'en'
                #
                # =================================================
                translated_fields=[
                    "profile.bio",
                ],
            ),
        )

        # =====================================================
        # MANUAL CUSTOM WHERE INJECTION
        # =====================================================
        # Used for advanced conditions not supported
        # automatically by helper
        #
        # Example:
        # (
        #   age > 18
        #   AND status='active'
        # )
        # OR
        # isSuperAdmin=true
        #
        # =====================================================
        .where(
            or_(
                and_(
                    User.age > 18,
                    User.status == "active",
                ),
                User.isSuperAdmin == True,
            )
        )

        # =====================================================
        # MANUAL EAGER LOADING
        # =====================================================
        # Additional performance optimization
        #
        # selectinload is VERY efficient
        #
        # =====================================================
        .options(
            selectinload(User.profile)
        )

        # =====================================================
        # MANUAL GROUP BY
        # =====================================================
        # Needed for aggregation queries
        #
        # =====================================================
        .group_by(User.id)

        # =====================================================
        # MANUAL HAVING
        # =====================================================
        # Used after GROUP BY
        #
        # =====================================================
        .having(
            func.count(User.id) > 0
        )

        # =====================================================
        # MANUAL EXTRA COLUMNS
        # =====================================================
        # Add calculated fields
        #
        # Example:
        # COUNT(users.id)
        #
        # =====================================================
        .add_columns(
            func.count(User.id).label("userCount")
        )

        # =====================================================
        # MANUAL RAW QUERY MODIFICATION
        # =====================================================
        # Full access to SQLAlchemy query
        #
        # MOST POWERFUL ESCAPE HATCH
        #
        # =====================================================
        .modify(
            lambda q: q.order_by(
                User.firstName.asc()
            )
        )
    )

    # =========================================================
    # EXECUTE QUERY
    # =========================================================
    # Returns:
    #
    # {
    #   "data": [...],
    #   "meta": {
    #       "total": 100,
    #       "page": 1,
    #       "limit": 10,
    #       "totalPages": 10,
    #       "hasNextPage": true,
    #       "hasPreviousPage": false
    #   }
    # }
    #
    # =========================================================
    result = await query.get_many_and_meta()

    # =========================================================
    # RETURN RESPONSE
    # =========================================================
    return result