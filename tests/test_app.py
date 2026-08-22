# tests/test_app.py — teste que chaque page du dashboard se rend sans exception,
# en mode Normal et en mode Crise.
# Lancer depuis la racine du repo : python -m tests.test_app  (ou pytest tests/)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest
from pages import PAGE_MODULES

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def run_all():
    any_error = False
    for page in PAGE_MODULES.keys():
        at = AppTest.from_file(APP_PATH)
        at.run(timeout=60)
        at.selectbox[0].select(page).run(timeout=60)
        if at.exception:
            any_error = True
            print(f"❌ {page} : EXCEPTION")
            for e in at.exception:
                print("   ", e)
        else:
            print(f"✅ {page} : OK")

        radios = [r for r in at.sidebar.radio if r.key and "mode" in r.key]
        if radios:
            radios[0].set_value("Crise").run(timeout=60)
            if at.exception:
                any_error = True
                print(f"❌ {page} (mode Crise) : EXCEPTION")
                for e in at.exception:
                    print("   ", e)
            else:
                print(f"✅ {page} (mode Crise) : OK")

    print("\nRÉSULTAT:", "ÉCHEC" if any_error else "TOUT OK")
    return not any_error


def test_all_pages_render_without_exception():
    """Point d'entrée pytest."""
    assert run_all()


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
