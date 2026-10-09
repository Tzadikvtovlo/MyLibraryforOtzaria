# -*- coding: utf-8 -*-
"""יוצר קישורים אוטומטית לספרים במאגר, בעזרת מנוע "מחולל הקישורים" (linker_core), ומאמת מול seforim.db הרשמי.

הקישורים נכתבים ל-<תיקיית קישורים>/קישורים/auto/links.csv, בפורמט ש-build_personal_db.py קורא.
ספרים שיש להם כבר קישורים משלהם (קבצי links.csv שהמשתמש העלה) לא נוגעים בהם.

שימוש: python auto_links.py <תיקיית ספרים> <seforim.db> [<תיקיית קישורים>]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linker_core as C


def main():
    books_dir, db_path = sys.argv[1], sys.argv[2]
    links_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(books_dir, 'קבצי קישורים וסדר הדורות')
    db = C.SeforimDB(db_path)
    plan = C.plan_repair(books_dir, links_dir, db, progress=print)
    adds = plan['additions']
    if not adds:
        print('לא נוצרו קישורים אוטומטיים (אין ספרים עם כלל יצירה מתאים)')
        return 0
    rows = []
    for stem, a in adds:
        rows.extend(a)
        print(f'  {stem}: {len(a)} קישורים')
    out = os.path.join(links_dir, 'קישורים', 'auto', 'links.csv')
    C.write_csv(out, rows)
    print(f'נוצרו קישורים ל-{len(adds)} ספרים ({len(rows)} שורות) ב-{out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
