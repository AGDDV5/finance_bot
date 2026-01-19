TEXTS = {
    'uz_lat': {
        'welcome': "👋 Assalomu alaykum! Moliyaviy yordamchingizga xush kelibsiz.\nIltimos, tilni tanlang:",
        'main_menu': "Asosiy menyu:",
        'choose_type': "Amaliyot turini tanlang:",
        'expense': "💸 Xarajat",
        'income': "💰 Daromad",
        'report': "📊 Hisobot",
        'settings': "⚙️ Sozlamalar",
        'choose_category': "Kategoriyani tanlang:",
        'food': "Oziq-ovqat",
        'utilities': "Kommunal",
        'housing': "Turar joy",
        'others': "Boshqalar",
        'salary': "Maosh",
        'enter_amount': "Summani kiriting (UZS):",
        'custom_cat_ask': "Bu xarajat qayerga ketdi?",
        'custom_source_ask': "Bu pul qayerdan keldi?",
        'success': "✅ Muvaffaqiyatli saqlandi!\n\n📂 Kategoriya: {}\n💰 Summa: {} UZS",
        'error_num': "⚠️ Iltimos, faqat raqam kiriting!",
        'dashboard_caption': "Sizning moliyaviy holatingiz (Joriy oy)",
        'btn_cancel': "Bekor qilish"
    },
    'uz_cyr': {
        'welcome': "👋 Ассалому алайкум! Молиявий ёрдамчингизга хуш келибсиз.\nИлтимос, тилни танланг:",
        'main_menu': "Асосий меню:",
        'choose_type': "Амалиёт турини танланг:",
        'expense': "💸 Харажат",
        'income': "💰 Даромад",
        'report': "📊 Ҳисобот",
        'settings': "⚙️ Созламалар",
        'choose_category': "Категорияни танланг:",
        'food': "Озиқ-овқат",
        'utilities': "Коммунал",
        'housing': "Турар жой",
        'others': "Бошқалар",
        'salary': "Маош",
        'enter_amount': "Суммани киритинг (UZS):",
        'custom_cat_ask': "Бу харажат қаерга кетди?",
        'custom_source_ask': "Бу пул қаердан келди?",
        'success': "✅ Муваффақиятли сақланди!\n\n📂 Категория: {}\n💰 Сумма: {} UZS",
        'error_num': "⚠️ Илтимос, фақат рақам киритинг!",
        'dashboard_caption': "Сизнинг молиявий ҳолатингиз (Жорий ой)",
        'btn_cancel': "Бекор қилиш"
    }
}

def get_text(lang, key):
    return TEXTS.get(lang, TEXTS['uz_lat']).get(key, key)