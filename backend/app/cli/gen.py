from pathlib import Path

import click

TEMPLATE_DIR = Path(__file__).parent / "templates"


def to_camel_case(snake_str: str) -> str:
    """snake_case -> CamelCase (例: sys_user -> SysUser)"""
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_kebab_case(snake_str: str) -> str:
    """snake_case -> kebab-case (例: sys_user -> sys-users)"""
    return snake_str.lower().replace("_", "-")


def read_template(template_name: str) -> str:
    """讀取指定模板文件內容"""
    template_path = TEMPLATE_DIR / f"{template_name}.py.tpl"
    if not template_path.exists():
        raise FileNotFoundError(f"找不到模板文件: {template_path}")
    return template_path.read_text(encoding="utf-8")


@click.group(name="gen", help="代碼生成器工具")
def gen_group() -> None:
    """代碼腳手架命令行"""
    pass


@gen_group.command(
    name="module", help="自動生成 Controller, Service, Schema 與 Model 腳手架"
)
@click.argument("name", type=str)
@click.option(
    "--tag",
    "-t",
    help="Swagger/API 文檔標籤中文名稱（例如：商品管理模塊）",
    default=None,
)
@click.option(
    "--path",
    "-p",
    help="生成業務模組文件的目標路徑（相對於 app/modules/system/）",
    default=None,
)
@click.option(
    "--models-dir",
    help="Model 檔案儲存的根目錄",
    default="app/db/models",
    show_default=True,
)
def generate_module(
    name: str, tag: str | None, path: str | None, models_dir: str
) -> None:
    """
    生成四層架構（Model, Schema, Service, Controller）代碼腳手架

    使用範例：
    python cli.py gen module article -t "文章管理模塊"
    """
    snake_name = name.lower().strip()
    pascal_name = to_camel_case(snake_name)
    kebab_name = to_kebab_case(snake_name)
    tag_name = tag or f"{pascal_name}模塊"

    # 目錄定義
    module_subpath = path if path else snake_name
    module_target_dir = Path("app/modules/system") / module_subpath
    models_target_dir = Path(models_dir)
    module_import_path = f"app.modules.system.{module_subpath.replace('/', '.')}"

    # 確認模組目錄與 Model 檔案是否存在
    model_file_path = models_target_dir / f"{snake_name}.py"

    if module_target_dir.exists() or model_file_path.exists():
        click.echo(click.style("⚠️  警告: 模組目錄或 Model 文件已存在！", fg="yellow"))
        click.echo(f"  模組目錄: {module_target_dir}")
        click.echo(f"  Model 文件: {model_file_path}")
        if not click.confirm("是否繼續生成並覆蓋檔案？"):
            click.echo(click.style("已取消生成操作。", fg="red"))
            return

    # 建立目錄
    module_target_dir.mkdir(parents=True, exist_ok=True)
    models_target_dir.mkdir(parents=True, exist_ok=True)

    # 渲染上下文參數字典
    context = {
        "snake_name": snake_name,
        "pascal_name": pascal_name,
        "kebab_name": kebab_name,
        "tag_name": tag_name,
        "module_import_path": module_import_path,
    }

    try:
        # 1. 生成 Model (預設儲存在 app/db/models/{snake_name}.py)
        model_tpl = read_template("model")
        rendered_model = model_tpl.format(**context)
        model_file_path.write_text(rendered_model.strip() + "\n", encoding="utf-8")
        click.echo(
            click.style(f"  [+] 已生成 Model 文件: {model_file_path}", fg="green")
        )

        # 2. 生成 Controller, Service, Schema 於業務目錄
        files_to_generate = {
            "schema.py": "schema",
            "service.py": "service",
            "controller.py": "controller",
        }

        for file_name, tpl_name in files_to_generate.items():
            raw_template = read_template(tpl_name)
            rendered_code = raw_template.format(**context)
            file_path = module_target_dir / file_name
            file_path.write_text(rendered_code.strip() + "\n", encoding="utf-8")
            click.echo(click.style(f"  [+] 已生成模組文件: {file_path}", fg="green"))

        # 3. 建立業務模組的 __init__.py
        init_file = module_target_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            click.echo(click.style(f"  [+] 已生成文件: {init_file}", fg="green"))

        click.echo(
            click.style(f"\n✨ 模組【{name}】腳手架生成完畢！", fg="cyan", bold=True)
        )

    except Exception as e:
        click.echo(click.style(f"\n❌ 生成失敗: {e}", fg="red"))
