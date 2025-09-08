# Simple dbt Notes for Students

## What is dbt?
dbt stands for data build tool. It's an open-source command-line tool that helps data teams transform data in their warehouses using SQL. It allows you to build, test, and document data models efficiently.

## Why Use dbt?
- Turns data transformation into a software engineering practice
- Enables version control for data pipelines
- Provides testing and documentation for data
- Works with popular data warehouses like Snowflake, BigQuery, Redshift, etc.

## Key Concepts
- **Models**: These are SQL SELECT statements that define your data transformations. Each model is a .sql file in the models/ directory. dbt compiles and runs them in the correct order based on dependencies.
  
- **Seeds**: CSV files that contain static data you want to load into your warehouse. Useful for lookup tables or reference data.

- **Snapshots**: Special models that capture changes in source data over time, like slowly changing dimensions.

- **Tests**: Built-in or custom assertions to validate your data. Run with `dbt test` to catch issues early.

- **Macros**: Reusable pieces of SQL code, like functions, to avoid repetition.

- **Sources**: Define and document your raw data tables for freshness checks and references.

## Jinja Templating in dbt
dbt uses Jinja, a templating engine, to make your SQL dynamic. This allows you to:
- Reference models with `{{ ref('model_name') }}` (resolves to the actual table/view name)
- Use variables, loops, and conditionals in SQL (e.g., {% if target.name == 'dev' %} ... {% endif %})
- Call macros like {{ my_macro() }}

Jinja helps make your dbt code more modular and adaptable to different environments.

## Basic Workflow
1. **Install dbt**: Use pip (e.g., `pip install dbt-core dbt-<adapter>`) where <adapter> is your warehouse (e.g., dbt-snowflake).

2. **Initialize a Project**: Run `dbt init` to create the project structure.

3. **Configure**: Set up profiles.yml (connection details) and dbt_project.yml (project settings).

4. **Develop Models**: Write SQL in models/*.sql. Use {{ ref('model_name') }} to reference other models.

5. **Run Commands**:
   - `dbt run`: Builds your models
   - `dbt test`: Runs tests
   - `dbt docs generate`: Creates documentation
   - `dbt compile`: Checks SQL without running

6. **Deploy**: Use dbt Cloud for scheduling or integrate with CI/CD.

## Best Practices
- Use meaningful names for models (e.g., stg_customers.sql, dim_customers.sql)
- Organize models in subfolders (staging, intermediate, marts)
- Always add descriptions and tests to models
- Use version control (Git) for your dbt project

## Sources
- Official dbt Documentation: https://docs.getdbt.com/docs/introduction
- dbt Learn Courses: https://courses.getdbt.com/
- dbt GitHub Repository: https://github.com/dbt-labs/dbt-core
- Getting Started Tutorial: https://docs.getdbt.com/tutorial/getting-started

These notes are simplified for beginners. Encourage students to practice with a sample project!
