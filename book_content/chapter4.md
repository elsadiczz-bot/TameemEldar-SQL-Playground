# الفصل 4: الربط

## 4.1 JOINs — الربط بين الجداول

### الأنواع
| النوع | المعنى |
|-------|--------|
| INNER JOIN | المتطابق فقط |
| LEFT JOIN | كل اليسار + المتطابق |
| RIGHT JOIN | كل اليمين + المتطابق |
| FULL JOIN | الكل |

### مثال 1: INNER JOIN

**الاستعلام:**
SELECT p.name, m.drug_name 
FROM patients p 
INNER JOIN medications m ON p.id = m.patient_id
LIMIT 5;

**النتيجة:**
| name | drug_name |
|------|-----------|
| Patient 1 | Metformin |
| Patient 1 | Insulin |
| Patient 2 | Amlodipine |
| Patient 3 | Salbutamol |
| Patient 3 | Prednisolone |

**ما يفعله:** يربط المرضى بالأدوية — يعرض فقط المتطابق.

### مثال 2: LEFT JOIN

**الاستعلام:**
SELECT p.name, m.drug_name 
FROM patients p 
LEFT JOIN medications m ON p.id = m.patient_id
LIMIT 7;

**النتيجة:**
| name | drug_name |
|------|-----------|
| Patient 1 | Metformin |
| Patient 1 | Insulin |
| Patient 2 | Amlodipine |
| Patient 3 | Salbutamol |
| Patient 3 | Prednisolone |
| Patient 6 | NULL |
| Patient 7 | NULL |

**ما يفعله:** يعرض كل المرضى — حتى بدون أدوية (NULL).
