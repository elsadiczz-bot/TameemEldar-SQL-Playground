"""
🎓TameemEldar SQL Playground Pro — مع بيانات حقيقية
تعلّم SQL على بياناتك الخاصة
"""

import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO


# ═══════════════════════════════════════════════════════
# 1. إدارة قاعدة البيانات (مع دعم البيانات الخارجية)
# ═══════════════════════════════════════════════════════
class DatabaseManager:
    """كل ما يتعلق بقاعدة البيانات — يدعم بيانات متعددة"""
    
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._init_default_tables()
        self.user_tables = []  # جداول المستخدم
    
    def _init_default_tables(self):
        """إنشاء الجداول الافتراضية"""
        patients = pd.DataFrame({
            "id": range(1, 21),
            "name": [f"Patient {i}" for i in range(1, 21)],
            "age": [25, 45, 60, 32, 55, 38, 72, 28, 50, 35,
                    42, 68, 30, 48, 52, 33, 65, 40, 58, 47],
            "gender": ["Male", "Female"] * 10,
            "diagnosis": ["Diabetes", "Hypertension", "Asthma", "Stroke", "Cancer"] * 4,
            "status": ["discharge", "dead", "DAMA", "discharge", "discharge"] * 4,
        })
        patients.to_sql("patients", self.conn, index=False, if_exists="replace")
        
        medications = pd.DataFrame({
            "id": range(1, 16),
            "patient_id": [1, 1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10],
            "drug_name": ["Metformin", "Insulin", "Amlodipine", "Salbutamol",
                          "Prednisolone", "Oxygen", "Aspirin", "Metformin",
                          "Insulin", "Amlodipine", "Aspirin", "Salbutamol",
                          "Metformin", "Prednisolone", "Oxygen"],
            "dose_mg": [500, 20, 5, 100, 40, 0, 75, 500, 25, 5, 75, 100, 500, 40, 0],
        })
        medications.to_sql("medications", self.conn, index=False, if_exists="replace")
    
    def add_user_table(self, df, table_name):
        """إضافة جدول من ملف المستخدم"""
        try:
            # تنظيف اسم الجدول
            clean_name = "".join(c if c.isalnum() or c == "_" else "_" for c in table_name)
            if not clean_name or clean_name[0].isdigit():
                clean_name = f"table_{clean_name}"
            
            df.to_sql(clean_name, self.conn, index=False, if_exists="replace")
            
            if clean_name not in self.user_tables:
                self.user_tables.append(clean_name)
            
            return clean_name, None
        except Exception as e:
            return None, str(e)
    
    def run(self, query):
        """تنفيذ استعلام SQL"""
        try:
            return pd.read_sql_query(query, self.conn), None
        except Exception as e:
            return None, str(e)
    
    def get_table(self, name):
        """جلب جدول كامل"""
        return pd.read_sql_query(f"SELECT * FROM {name}", self.conn)
    
    def list_all_tables(self):
        """قائمة كل الجداول"""
        result = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'",
            self.conn
        )
        return result["name"].tolist()
    
    def get_table_info(self, name):
        """معلومات الجدول — الأعمدة، الصفوف"""
        try:
            df = pd.read_sql_query(f"SELECT * FROM {name} LIMIT 1", self.conn)
            count = pd.read_sql_query(f"SELECT COUNT(*) as c FROM {name}", self.conn)["c"][0]
            return {
                "columns": list(df.columns),
                "rows": count
            }
        except:
            return None
    
    def delete_user_table(self, name):
        """حذف جدول المستخدم"""
        try:
            pd.read_sql_query(f"DROP TABLE IF EXISTS {name}", self.conn)
            if name in self.user_tables:
                self.user_tables.remove(name)
            return True, None
        except Exception as e:
            return False, str(e)


# ═══════════════════════════════════════════════════════
# 2. إدارة الدروس (نفس الشيء)
# ═══════════════════════════════════════════════════════
class LessonManager:
    """كل الدروس في مكان واحد"""
    
    def __init__(self):
        self.lessons = {
            "1_select": {
                "title": "1️⃣ SELECT — استخراج البيانات",
                "difficulty": "🟢 مبتدئ",
                "simple": "SELECT = اختر. يختار الأعمدة التي تريد عرضها من الجدول.",
                "deep": "SELECT هو أساس كل استعلام في SQL. الصيغة: SELECT column1, column2 FROM table_name; — يمكنك استخدام * لكل الأعمدة، أو AS لإعطاء اسم بديل، أو DISTINCT لإزالة التكرار.",
                "examples": [
                    "SELECT * FROM patients;",
                    "SELECT name FROM patients;",
                    "SELECT name, age FROM patients;",
                    "SELECT DISTINCT diagnosis FROM patients;",
                ],
                "example_query": "SELECT name, age FROM patients LIMIT 5",
            },
            "2_where": {
                "title": "2️⃣ WHERE — التصفية",
                "difficulty": "🟢 مبتدئ",
                "simple": "WHERE = أين. يفلتر الصفوف حسب شرط معين.",
                "deep": "WHERE يستخدم للمقارنة: = , > , < , != . يمكن استخدام AND, OR . IN لقائمة، BETWEEN لنطاق، LIKE للنمط.",
                "examples": [
                    "SELECT * FROM patients WHERE age > 50;",
                    "SELECT * FROM patients WHERE gender = 'Male';",
                    "SELECT * FROM patients WHERE age > 50 AND gender = 'Male';",
                    "SELECT * FROM patients WHERE diagnosis IN ('Diabetes', 'Stroke');",
                    "SELECT * FROM patients WHERE age BETWEEN 40 AND 60;",
                ],
                "example_query": "SELECT * FROM patients WHERE age > 50",
            },
            "3_order": {
                "title": "3️⃣ ORDER BY — الترتيب",
                "difficulty": "🟢 مبتدئ",
                "simple": "ORDER BY = رتّب حسب. يرتب النتائج تصاعدياً أو تنازلياً.",
                "deep": "ORDER BY column ASC (تصاعدي) أو DESC (تنازلي). يمكن الترتيب بعدة أعمدة.",
                "examples": [
                    "SELECT * FROM patients ORDER BY age;",
                    "SELECT * FROM patients ORDER BY age DESC;",
                    "SELECT * FROM patients ORDER BY age DESC LIMIT 5;",
                ],
                "example_query": "SELECT name, age FROM patients ORDER BY age DESC LIMIT 5",
            },
            "4_aggregations": {
                "title": "4️⃣ Aggregations — التجميع",
                "difficulty": "🟡 متوسط",
                "simple": "Aggregations تحوّل صفوفاً كثيرة إلى قيمة واحدة (عد، مجموع، متوسط).",
                "deep": "COUNT() للعد، SUM() للمجموع، AVG() للمتوسط، MIN() للأصغر، MAX() للأكبر. تُستخدم مع GROUP BY.",
                "examples": [
                    "SELECT COUNT(*) FROM patients;",
                    "SELECT AVG(age) FROM patients;",
                    "SELECT MIN(age), MAX(age) FROM patients;",
                    "SELECT COUNT(*) as total, AVG(age) as avg_age FROM patients;",
                ],
                "example_query": "SELECT COUNT(*) as total, AVG(age) as avg_age FROM patients",
            },
            "5_group_by": {
                "title": "5️⃣ GROUP BY — التجميع",
                "difficulty": "🟡 متوسط",
                "simple": "GROUP BY يجمع الصفوف المتشابهة في مجموعات.",
                "deep": "GROUP BY يُستخدم مع Aggregations. HAVING يفلتر المجموعات (بعد التجميع).",
                "examples": [
                    "SELECT diagnosis, COUNT(*) FROM patients GROUP BY diagnosis;",
                    "SELECT gender, AVG(age) FROM patients GROUP BY gender;",
                    "SELECT diagnosis, COUNT(*) FROM patients GROUP BY diagnosis HAVING COUNT(*) > 3;",
                ],
                "example_query": "SELECT diagnosis, COUNT(*) as count FROM patients GROUP BY diagnosis",
            },
            "6_joins": {
                "title": "6️⃣ JOINs — الربط",
                "difficulty": "🟡 متوسط",
                "simple": "JOIN يربط جدولين معاً حسب عمود مشترك.",
                "deep": "INNER JOIN: المتطابق فقط. LEFT JOIN: كل اليسار + المتطابق. الصيغة: FROM table1 JOIN table2 ON table1.col = table2.col",
                "examples": [
                    "SELECT p.name, m.drug_name FROM patients p JOIN medications m ON p.id = m.patient_id;",
                    "SELECT p.name, m.drug_name FROM patients p LEFT JOIN medications m ON p.id = m.patient_id;",
                ],
                "example_query": "SELECT p.name, m.drug_name FROM patients p JOIN medications m ON p.id = m.patient_id LIMIT 10",
            },
            "7_subqueries": {
                "title": "7️⃣ Subqueries — استعلامات فرعية",
                "difficulty": "🔴 متقدم",
                "simple": "Subquery = استعلام داخل استعلام آخر.",
                "deep": "Subquery يُنفَّذ أولاً، ثم النتيجة تُستخدم في الخارجي. مثال: WHERE age > (SELECT AVG(age) FROM patients)",
                "examples": [
                    "SELECT * FROM patients WHERE age > (SELECT AVG(age) FROM patients);",
                    "SELECT * FROM patients WHERE id IN (SELECT patient_id FROM medications);",
                ],
                "example_query": "SELECT * FROM patients WHERE age > (SELECT AVG(age) FROM patients)",
            },
            "8_cte": {
                "title": "8️⃣ CTEs — الجداول المؤقتة",
                "difficulty": "🔴 متقدم",
                "simple": "CTE = جدول مؤقت يُسمّى، باستخدام WITH.",
                "deep": "WITH cte_name AS (SELECT ...) SELECT * FROM cte_name; — يجعل الاستعلامات المعقدة أوضح.",
                "examples": [
                    "WITH avg_cte AS (SELECT AVG(age) as avg_age FROM patients) SELECT * FROM patients WHERE age > (SELECT avg_age FROM avg_cte);",
                ],
                "example_query": "WITH avg_cte AS (SELECT AVG(age) as avg_age FROM patients) SELECT * FROM patients WHERE age > (SELECT avg_age FROM avg_cte)",
            },
            "9_case": {
                "title": "9️⃣ CASE WHEN — الشروط",
                "difficulty": "🟡 متوسط",
                "simple": "CASE WHEN = if/else داخل SQL.",
                "deep": "CASE WHEN condition THEN result ELSE default END — لتصنيف البيانات.",
                "examples": [
                    "SELECT name, age, CASE WHEN age < 30 THEN 'Young' WHEN age < 60 THEN 'Middle' ELSE 'Old' END as age_group FROM patients;",
                ],
                "example_query": "SELECT name, age, CASE WHEN age < 30 THEN 'Young' WHEN age < 60 THEN 'Middle' ELSE 'Old' END as grp FROM patients",
            },
            "10_window": {
                "title": "🔟 Window Functions — دوال النوافذ",
                "difficulty": "🔴 متقدم",
                "simple": "Window Functions تحسب على مجموعة لكن تُرجع صفاً لكل صف.",
                "deep": "ROW_NUMBER() OVER (ORDER BY ...) — رقم الصف. RANK() — الترتيب. LAG/LEAD — القيمة السابقة/التالية.",
                "examples": [
                    "SELECT name, age, ROW_NUMBER() OVER (ORDER BY age DESC) as rank FROM patients;",
                ],
                "example_query": "SELECT name, age, ROW_NUMBER() OVER (ORDER BY age DESC) as rank FROM patients",
            },
        }
    
    def get_titles(self):
        return [l["title"] for l in self.lessons.values()]
    
    def get_by_title(self, title):
        for lesson in self.lessons.values():
            if lesson["title"] == title:
                return lesson
        return None


# ═══════════════════════════════════════════════════════
# 3. إدارة التحديات
# ═══════════════════════════════════════════════════════
class ChallengeManager:
    """كل التحديات في مكان واحد"""
    
    def __init__(self):
        self.challenges = [
            {"level": "🟢", "q": "اعرض كل أسماء المرضى",
             "hint": "SELECT name FROM patients",
             "sol": "SELECT name FROM patients"},
            {"level": "🟢", "q": "اعرض المرضى أكبر من 50",
             "hint": "WHERE age > 50",
             "sol": "SELECT * FROM patients WHERE age > 50"},
            {"level": "🟢", "q": "اعرض المرضى الذكور",
             "hint": "WHERE gender = 'Male'",
             "sol": "SELECT * FROM patients WHERE gender = 'Male'"},
            {"level": "🟢", "q": "أعلى 5 مرضى عمراً",
             "hint": "ORDER BY DESC LIMIT 5",
             "sol": "SELECT * FROM patients ORDER BY age DESC LIMIT 5"},
            {"level": "🟡", "q": "احسب عدد المرضى",
             "hint": "COUNT(*)",
             "sol": "SELECT COUNT(*) FROM patients"},
            {"level": "🟡", "q": "التشخيصات المختلفة",
             "hint": "DISTINCT",
             "sol": "SELECT DISTINCT diagnosis FROM patients"},
            {"level": "🟡", "q": "عدد المرضى لكل تشخيص",
             "hint": "GROUP BY",
             "sol": "SELECT diagnosis, COUNT(*) FROM patients GROUP BY diagnosis"},
            {"level": "🟡", "q": "اسم المريض + الدواء",
             "hint": "JOIN",
             "sol": "SELECT p.name, m.drug_name FROM patients p JOIN medications m ON p.id = m.patient_id"},
            {"level": "🔴", "q": "المرضى فوق متوسط الأعمار",
             "hint": "Subquery",
             "sol": "SELECT * FROM patients WHERE age > (SELECT AVG(age) FROM patients)"},
            {"level": "🔴", "q": "التشخيصات فيها أكثر من 3 مرضى",
             "hint": "HAVING",
             "sol": "SELECT diagnosis, COUNT(*) FROM patients GROUP BY diagnosis HAVING COUNT(*) > 3"},
            {"level": "🔴", "q": "ترتيب المرضى حسب العمر",
             "hint": "ROW_NUMBER()",
             "sol": "SELECT name, age, ROW_NUMBER() OVER (ORDER BY age DESC) as rank FROM patients"},
        ]
    
    def get_titles(self):
        return [f"{c['level']} — {c['q']}" for c in self.challenges]
    
    def get_by_title(self, title):
        for c in self.challenges:
            if c['q'] in title:
                return c
        return None


# ═══════════════════════════════════════════════════════
# 4. التطبيق الرئيسي
# ═══════════════════════════════════════════════════════
class SQLPlaygroundApp:
    """التطبيق الكامل"""
    
    def __init__(self):
        st.set_page_config(
            page_title="TameemEldar SQL Playground Pro",
            page_icon="logo_full.png.png",  # ← الشعار
            layout="wide"
        )
        
        self.db = self._get_db()
        self.lessons = LessonManager()
        self.challenges = ChallengeManager()
    
    @staticmethod
    @st.cache_resource
    def _get_db():
        return DatabaseManager()
    
    # ─── عناصر مشتركة ───
    @staticmethod
    @staticmethod
    def render_title():
        """عنوان التطبيق — مع الشعار"""
        col1, col2 = st.columns([1, 6])
    
        with col1:
            try:
                st.image("log_icon.png.png", width=100)
            except:
                st.markdown("# 🎓")
    
        with col2:
            st.title("TameemEldar SQL Playground Pro")
            st.markdown("**تعلّم SQL على بياناتك الحقيقية**")

    
    def render_query_result(self, query, key):
        if st.button("▶️ نفّذ", type="primary", key=f"btn_{key}"):
            result, error = self.db.run(query)
            if error:
                st.error(f"❌ {error}")
            else:
                st.success(f"✅ {len(result)} صف")
                st.dataframe(result, use_container_width=True)
    
    # ─── إدارة البيانات ───
    def render_book_tab(self):
        """Tab: كتاب SQL الكامل"""
        st.header("📖 كتاب SQL الكامل")
        st.markdown("**دليلك الشامل لتعلّم SQL — من الصفر للاحتراف**")
    
        # فهرس الكتاب
        st.markdown("### 📚 محتوى الكتاب:")
    
        chapters = {
            "1": "مقدمة — ما هو SQL؟ لماذا SQL؟",
            "2": "الأساسيات — SELECT, WHERE, ORDER BY, LIMIT",
            "3": "التجميع — Aggregations, GROUP BY, HAVING",
            "4": "الربط — JOINs, UNION, Subqueries",
            "5": "المتقدم — CTEs, CASE WHEN, Window Functions, Indexes",
            "6": "الخلاصة — ملخص المهارات والخطوات القادمة",
    }
    
        for num, title in chapters.items():
            st.markdown(f"- **الفصل {num}:** {title}")
    
        st.markdown("---")
    
        # اختيار الفصل
        st.markdown("### 📖 اختر فصلاً للقراءة:")
    
        chapter_choice = st.selectbox(
            "الفصل:",
            ["الفصل 1: مقدمة", "الفصل 2: الأساسيات", 
             "الفصل 3: التجميع", "الفصل 4: الربط",
             "الفصل 5: المتقدم", "الفصل 6: الخلاصة"]
        )
    
        # رقم الفصل
        chapter_num = chapter_choice.split(":")[0].replace("الفصل ", "").strip()
    
        # تحميل محتوى الفصل
        chapter_file = f"book_content/chapter{chapter_num}.md"
    
        try:
            with open(chapter_file, "r", encoding="utf-8") as f:
               content = f.read()
        
            # عرض الفصل
            with st.container():
                st.markdown(content)
    
        except FileNotFoundError:
            st.warning(f"⚠️ ملف الفصل غير موجود: {chapter_file}")
            st.info("💡 تأكد من إنشاء مجلد `book_content` ووضع ملفات الفصول فيه.")
    
        except Exception as e:
            st.error(f"❌ خطأ: {e}")
    
        st.markdown("---")
    
        
        # إحصاءات
        st.markdown("### 📊 إحصاءات الكتاب:")
    
        col1, col2, col3 = st.columns(3)
        col1.metric("📚 الفصول", "6")
        col2.metric("📝 الأمثلة", "25+")
        col3.metric("🎯 المواضيع", "10")

    def render_data_manager(self):
        """Tab: إدارة البيانات — رفع ملفات"""
        st.header("📂 إدارة البيانات")
        st.markdown("**ارفع ملف Excel أو CSV — وحلّله بـ SQL**")
        
        # رفع الملف
        uploaded_file = st.file_uploader(
            "اختر ملفاً:",
            type=["xlsx", "xls", "csv"],
            help="يدعم Excel و CSV"
        )
        
        if uploaded_file:
            try:
                # قراءة الملف
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ تم تحميل: **{uploaded_file.name}**")
                
                # معلومات الملف
                col1, col2, col3 = st.columns(3)
                col1.metric("📁 الصفوف", len(df))
                col2.metric("📋 الأعمدة", len(df.columns))
                col3.metric("💾 الحجم", f"{uploaded_file.size / 1024:.1f} KB")
                
                st.markdown("---")
                
                # اسم الجدول
                default_name = uploaded_file.name.replace(".xlsx", "").replace(".xls", "").replace(".csv", "")
                default_name = "".join(c if c.isalnum() or c == "_" else "_" for c in default_name)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    table_name = st.text_input("اسم الجدول:", value=default_name)
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("📥 **حمّل الجدول**", type="primary", use_container_width=True):
                        with st.spinner("جاري التحميل..."):
                            clean_name, error = self.db.add_user_table(df, table_name)
                            if error:
                                st.error(f"❌ {error}")
                            else:
                                st.success(f"✅ تم! الجدول: **{clean_name}**")
                                st.rerun()
                
                # معاينة
                st.markdown("### 📋 معاينة البيانات:")
                st.dataframe(df.head(10), use_container_width=True)
                
                # الأعمدة
                st.markdown("### 📊 الأعمدة:")
                st.code(", ".join(df.columns), language="sql")
                
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {e}")
        
        # الجداول الحالية
        st.markdown("---")
        st.markdown("## 📊 الجداول المتاحة")
        
        all_tables = self.db.list_all_tables()
        
        for table in all_tables:
            info = self.db.get_table_info(table)
            if info:
                is_user_table = table in self.db.user_tables
                icon = "📂" if is_user_table else "🎓"
                
                with st.expander(f"{icon} **{table}** — {info['rows']} صف، {len(info['columns'])} عمود"):
                    st.markdown(f"**الأعمدة:**")
                    st.code(", ".join(info["columns"]), language="sql")
                    
                    # عرض البيانات
                    df = self.db.get_table(table)
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # زر الحذف (لجداول المستخدم فقط)
                    if is_user_table:
                        if st.button(f"🗑️ حذف **{table}**", key=f"del_{table}"):
                            success, error = self.db.delete_user_table(table)
                            if success:
                                st.success(f"✅ تم حذف {table}")
                                st.rerun()
                            else:
                                st.error(f"❌ {error}")
   
    # ─── التبويبات ───
    def render_learn_tab(self):
        st.header("📚 تعلّم SQL خطوة بخطوة")
        
        selected = st.selectbox("اختر درساً:", self.lessons.get_titles())
        lesson = self.lessons.get_by_title(selected)
        
        if not lesson:
            return
        
        st.markdown(f"**المستوى:** {lesson['difficulty']}")
        st.markdown("---")
        
        with st.expander("💡 شرح مبسط", expanded=True):
            st.markdown(lesson["simple"])
        
        with st.expander("📖 شرح عميق", expanded=False):
            st.markdown(lesson["deep"])
        
        st.markdown("### 📝 أمثلة:")
        for ex in lesson["examples"]:
            st.code(ex, language="sql")
        
        st.markdown("---")
        st.markdown("### 💻 جرّب بنفسك:")
        
        query = st.text_area(
            "اكتب SQL:",
            value=lesson["example_query"],
            height=120,
            key=f"learn_{selected}"
        )
        
        self.render_query_result(query, selected)
    
    def render_practice_tab(self):
        st.header("🎮 تحديات متدرجة")
        st.markdown("**حل التحديات — من السهل للصعب**")
        
        selected = st.selectbox("اختر تحدياً:", self.challenges.get_titles())
        current = self.challenges.get_by_title(selected)
        
        if not current:
            return
        
        st.markdown(f"### {current['level']} {current['q']}")
        st.info(f"💡 **تلميح:** {current['hint']}")
        
        query = st.text_area("اكتب حلك:", height=100, key=f"ch_{current['q']}")
        
        col1, col2 = st.columns(2)
        with col1:
            self.render_query_result(query, current['q'])
        with col2:
            if st.button("👁️ اظهر الحل", key=f"sol_{current['q']}"):
                st.code(current['sol'], language="sql")
    
    def render_explore_tab(self):
        st.header("🔍 SQL Playground")
        st.markdown("**اكتب أي استعلام — بحرية تامة**")
        
        # الجداول المتاحة
        all_tables = self.db.list_all_tables()
        
        st.markdown("### 📊 الجداول المتاحة:")
        
        cols = st.columns(min(len(all_tables), 3))
        for i, table in enumerate(all_tables):
            info = self.db.get_table_info(table)
            if info:
                with cols[i % 3]:
                    st.markdown(f"**{table}**")
                    st.caption(f"{info['rows']} صف × {len(info['columns'])} عمود")
                    st.code(", ".join(info["columns"][:4]) + ("..." if len(info["columns"]) > 4 else ""))
        
        st.markdown("---")
        
        query = st.text_area(
            "اكتب SQL:",
            value=f"SELECT * FROM {all_tables[0] if all_tables else 'patients'} LIMIT 10",
            height=200,
            key="playground"
        )
        
        self.render_query_result(query, "pg")
    
    def render_sidebar(self):
        with st.sidebar:
            st.markdown("## 🎓 SQL Playground Pro")
            st.markdown("---")
            
            # عدد الجداول
            all_tables = self.db.list_all_tables()
            user_count = len(self.db.user_tables)
            
            st.markdown(f"### 📊 الجداول ({len(all_tables)}):")
            st.markdown(f"- 🎓 تدريبية: **{len(all_tables) - user_count}**")
            st.markdown(f"- 📂 بياناتك: **{user_count}**")
            
            st.markdown("---")
            st.markdown("### 💡 نصيحة:")
            st.info("""
            **للبيانات الحقيقية:**
            1. اذهب لتبويب "📂 البيانات"
            2. ارفع ملف Excel/CSV
            3. سمّ الجدول
            4. ابدأ التحليل!
            """)
    
    # ─── التشغيل ───
    def run(self):
        """التشغيل الكامل"""
        self.render_title()
        self.render_sidebar()
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📚 تعلّم", 
            "🎮 تدرّب", 
            "🔍 استكشف", 
            "📂 البيانات", 
            "📊 التدريبية",
            "📖 الكتاب"
        ])
                
        with tab1:
            self.render_learn_tab()
        with tab2:
            self.render_practice_tab()
    
        with tab3:
            self.render_explore_tab()
        with tab4:
            self.render_data_manager()
        with tab5:
            st.header("📊 البيانات التدريبية")
            st.markdown("**بيانات جاهزة للتعلّم**")
                    
            table = st.selectbox("اختر جدولاً:", ["patients", "medications"])
            df = self.db.get_table(table)
                    
            st.markdown(f"### 📋 {table}")
            st.markdown(f"**الصفوف:** {len(df)} | **الأعمدة:** {len(df.columns)}")
            st.dataframe(df, use_container_width=True)
        with tab6:
            self.render_book_tab() 
       

# ═══════════════════════════════════════════════════════
# نقطة البداية
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = SQLPlaygroundApp()
    app.run()
