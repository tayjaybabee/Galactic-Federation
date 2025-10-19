# Galactic Federation

A satirical-serious **NationStates-style** governance simulator set in space. Create a planet-state,
answer daily issues, watch stats swing, join sectors (regions), and vote in the Galactic Assembly.

## Quickstart

```bash
poetry install
cp .env.example .env
# Edit .env with your DB + Redis details
poetry run uvicorn galactic_federation.api.main:app --reload
```

Migrations:
```bash
poetry run alembic upgrade head
```

Workers:
```bash
poetry run celery -A galactic_federation.jobs.worker.celery_app worker -l info
poetry run celery -A galactic_federation.jobs.worker.celery_app beat -l info
```

## Concepts
- **Planet**: your playable identity (nation analogue).
- **Issue**: a dilemma with options that apply **effects** (data-driven) to stats.
- **Sector**: social grouping (region analogue) with a message wall.
- **Assembly**: interstellar vote/resolution system.

## License
Pick your poison (MIT/BSD-3/Apache-2.0). Don’t use NationStates assets/text.
