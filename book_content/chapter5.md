# الفصل 5: المتقدم

## 5.1 CTEs — الجداول المؤقتة

### التعريف
CTE = جدول مؤقت يُسمّى — باستخدام WITH.

### مثال

**الاستعلام:**
WITH avg_cte AS (
    SELECT AVG(age) as avg_age FROM patients
)
SELECT id, name, age, diagnosis 
FROM patients 
WHERE age > (SELECT avg_age FROM avg_cte)
LIMIT 3;

**النتيجة:**
| id | name | age | diagnosis |
|----|------|-----|-----------|
| 3 | Patient 3 | 60 | Asthma |
| 5 | Patient 5 | 55 | Cancer |
| 7 | Patient 7 | 72 | Hypertension |

**ما يفعله:** 
1. يحسب متوسط الأعمار
2. يعرض المرضى فوق المتوسط

## 5.2 CASE WHEN — الشروط

### التعريف
CASE WHEN = if/else داخل SQL.

### مثال: تصنيف الأعمار

**الاستعلام:**
SELECT name, age,
    CASE
        WHEN age < 30 THEN 'Young'
        WHEN age < 60 THEN 'Middle'
        ELSE 'Old'
    END as age_group
FROM patients
LIMIT 4;

**النتيجة:**
| name | age | age_group |
|------|-----|-----------|
| Patient 1 | 25 | Young |
| Patient 2 | 45 | Middle |
| Patient 3 | 60 | Old |
| Patient 4 | 32 | Middle |

**ما يفعله:** يضيف عمود "الفئة العمرية".

## 5.3 Window Functions — دوال النوافذ

### التعريف
تحسب على مجموعة — لكن تُرجع صفاً لكل صف.

### مثال: ترتيب حسب العمر

**الاستعلام:**
SELECT name, age,
    ROW_NUMBER() OVER (ORDER BY age DESC) as rank
FROM patients
LIMIT 4;

**النتيجة:**
| name | age | rank |
|------|-----|------|
| Patient 7 | 72 | 1 |
| Patient 12 | 68 | 2 |
| Patient 17 | 65 | 3 |
| Patient 3 | 60 | 4 |

**ما يفعله:** يضيف رقم ترتيب لكل مريض.

## 5.4 Indexes — الفهارس

### التعريف
Index = فهرس. يُسرّع البحث.

### مثال

**الاستعلام:**
CREATE INDEX idx_patient_name ON patients(name);

**النتيجة:**
✅ Index created

**الفرق:**
| بدون Index | مع Index |
|-----------|----------|
| O(n) — بطيء | O(log n) — سريع |
| يفحص كل الصف | بحث مباشر |
