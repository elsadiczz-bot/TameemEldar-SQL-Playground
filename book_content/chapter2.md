# الفصل 2: الأساسيات

## 2.1 SELECT — استخراج البيانات

### التعريف
SELECT = اختر. يختار الأعمدة.

### الصيغة
SELECT [DISTINCT] column1, column2 FROM table_name;

### الرموز
| الرمز | المعنى |
|-------|--------|
| `*` | كل الأعمدة |
| `AS` | اسم بديل |
| `DISTINCT` | إزالة التكرار |

### مثال 1: كل الأعمدة

**الاستعلام:**
SELECT * FROM patients LIMIT 3;

**النتيجة:**
| id | name | age | gender | diagnosis |
|----|------|-----|--------|-----------|
| 1 | Patient 1 | 25 | Male | Diabetes |
| 2 | Patient 2 | 45 | Female | Hypertension |
| 3 | Patient 3 | 60 | Male | Asthma |

**ما يفعله:** يعرض 3 صفوف بكل الأعمدة.

### مثال 2: عمود واحد

**الاستعلام:**
SELECT name FROM patients LIMIT 5;

**النتيجة:**
| name |
|------|
| Patient 1 |
| Patient 2 |
| Patient 3 |
| Patient 4 |
| Patient 5 |

## 2.2 WHERE — التصفية

### التعريف
WHERE = أين. يفلتر الصفوف.

### المعاملات
| المعامل | المعنى |
|---------|--------|
| `=` | يساوي |
| `>` | أكبر |
| `<` | أصغر |
| `!=` | لا يساوي |
| `AND` | و |
| `OR` | أو |
| `IN` | ضمن قائمة |
| `BETWEEN` | بين قيمتين |
| `LIKE` | يشبه |

### مثال: تصفية بسيطة

**الاستعلام:**
SELECT name, age FROM patients WHERE age > 50;

**النتيجة:**
| name | age |
|------|-----|
| Patient 3 | 60 |
| Patient 5 | 55 |
| Patient 7 | 72 |
| Patient 12 | 68 |

**ما يفعله:** يعرض المرضى فوق 50 سنة فقط.
