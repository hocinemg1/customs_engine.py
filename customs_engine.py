"""
=============================================================================
 نظام المحاكاة الجمركية الذكي - Business Gate DZ (Customs Simulation Engine)
 إشراف الخبير: أستاذ حوسين (خبرة 27 سنة في الإطار الجمركي والتشريعات)
 يعتمد على القواعد الست لتفسير النظام المنسق (RGI) ومعايير التعريفة الجمركية.
=============================================================================
"""

class CustomsClassificationEngine:
    def __init__(self):
        # قاعدة بيانات افتراضية تجريبية للبنود والرسوم (قابلة للتوسيع لتشمل التعريفة الكاملة)
        self.tariff_database = {
            "machinery": {
                "code_sh": "84.22",
                "description": "آلات ومعدات الرفع أو المناولة أو التحميل",
                "customs_duty_dd": 5.0,  # حقوق الجمارك %
                "tva": 19.0,             # الرسم على القيمة المضافة %
                "aapi_eligible": True    # مؤهل للإعفاءات الاستثمارية
            },
            "electronics": {
                "code_sh": "85.17",
                "description": "أجهزة الاتصالات الهاتفية واللاسلكية",
                "customs_duty_dd": 15.0,
                "tva": 19.0,
                "aapi_eligible": False
            },
            "raw_materials": {
                "code_sh": "39.01",
                "description": "بوليمرات الإيثيلين بأشكالها الأولية (مواد خام)",
                "customs_duty_dd": 0.0,
                "tva": 9.0,
                "aapi_eligible": True
            }
        }

    def apply_rgi_rules(self, item_name, state="finished", composition="single"):
        """
        محاكاة تطبيق القواعد الست لتفسير النظام المنسق (RGI 1 to 6):
        - القاعدة 1: التسمية الصريحة.
        - القاعدة 2: البضائع غير التامة أو المركبة (المخاليط).
        - القاعدة 3: الوصف الأكثر تحديداً والطابع الغالب.
        """
        print([*] جاري تحليل السلعة عبر محرك القواعد الست (RGI 1-6)...)
        
        # محاكاة تطبيق القاعدة 2 (ب) و 3 (الطابع الغالب والمواد المركبة)
        if composition == "mixture":
            print(-> تم رصد مادة مركبة: يُطبق التسلسل الهرمي (الطابع الغالب / الوصف الأكثر تحديداً - القاعدة 3).
        
        if state == "incomplete":
            print(-> تم رصد سلعة غير تامة الصنع: تُعامل معاملة التامة إذا كانت لها خصائصها الأساسية (القاعدة 2-أ).)

        # مطابقة مبدئية مع قاعدة البيانات للبحث عن البند الأنسب (القاعدة 1 و 6)
        matched_category = None
        for key, data in self.tariff_database.items():
            if key in item_name.lower() or data["description"].lower() in item_name.lower():
                matched_category = data
                break
        
        return matched_category

    def calculate_duties_and_taxes(self, item_name, cif_value_dzd, state="finished", composition="single", has_aapi=False):
        """
        حساب دقيق للحقوق والرسوم الجمركية بناءً على البند والتشريعات المعمول بها (بما فيها إعفاءات AAPI).
        """
        item_data = self.apply_rgi_rules(item_name, state, composition)
        
        if not item_data:
            return {
                "status": "Error",
                "message": "عذراً، لم يتم العثور على بند مطابق بدقة. يرجى إدخال تفاصيل تقنية أوسع لتطبيق القاعدة 4 أو 5."
            }

        dd_rate = item_data["customs_duty_dd"]
        tva_rate = item_data["tva"]

        # تطبيق إعفاءات الوكالة الوطنية لترقية الاستثمار AAPI إن توفرت شروط الاستثمار
        if has_aapi and item_data["aapi_eligible"]:
            dd_rate = 0.0
            exemption_note = "مستفيد من الإعفاء الجمركي الكلي/الجزئي في إطار استثمارات AAPI."
        else:
            exemption_note = "خاضع للحقوق والرسوم العامة العادية."

        # حساب المبالغ
        customs_duty_amount = cif_value_dzd * (dd_rate / 100.0)
        base_tva = cif_value_dzd + customs_duty_amount
        tva_amount = base_tva * (tva_rate / 100.0)
        total_fees = customs_duty_amount + tva_amount

        result = {
            "status": "Success",
            "item_description": item_data["description"],
            "code_sh": item_data["code_sh"],
            "cif_value": cif_value_dzd,
            "customs_duty_rate_percent": dd_rate,
            "customs_duty_amount": customs_duty_amount,
            "tva_rate_percent": tva_rate,
            "tva_amount": tva_amount,
            "total_estimated_taxes": total_fees,
            "regulatory_note": exemption_note
        }
        
        return result

# --- مثال تجريبي لاختبار الكود ---
if __name__ == "__main__":
    engine = CustomsClassificationEngine()
    
    # محاكاة إدخال استيراد آلات ومعدات بقيمة 10,000,000 دج مع امتيازات استثمارية
    simulation_result = engine.calculate_duties_and_taxes(
        item_name="machinery", 
        cif_value_dzd=10000000.0, 
        state="finished", 
        composition="single", 
        has_aapi=True
    )
    
    print("\n================ تقرير المحاكاة الجمركية الرسمي ================")
    for key, val in simulation_result.items():
        print(f"{key}: {val}")
    print("===============================================================")
