from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRODUCTS, REVIEWS_URL, SUPPORT_URL

def main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Главное меню бота"""
    keyboard = [
        [InlineKeyboardButton(text="🛍 Каталог промтов", callback_data="catalog")],
        [
            InlineKeyboardButton(text="⭐️ Отзывы", url=REVIEWS_URL),
            InlineKeyboardButton(text="💬 Поддержка", url=SUPPORT_URL)
        ]
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton(text="👑 Админ-панель", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def catalog_keyboard() -> InlineKeyboardMarkup:
    """Список всех доступных товаров"""
    keyboard = []
    for key, item in PRODUCTS.items():
        btn_text = f"{item['name']} — {item['price_rub']} ₽ / {item['price_stars']} ⭐️"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=f"prod:{key}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_detail_keyboard(product_key: str, price_stars: int, price_rub: int) -> InlineKeyboardMarkup:
    """Выбор способа оплаты в карточке товара"""
    keyboard = [
        [InlineKeyboardButton(text=f"⭐️ Оплатить Звёздами ({price_stars} ⭐️)", callback_data=f"buy_stars:{product_key}")],
        [InlineKeyboardButton(text=f"💳 Оплатить на Карту ({price_rub} ₽)", callback_data=f"buy_card:{product_key}")],
        [
            InlineKeyboardButton(text="⬅️ В каталог", callback_data="catalog"),
            InlineKeyboardButton(text="🏠 Меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def card_payment_keyboard(product_key: str) -> InlineKeyboardMarkup:
    """Клавиатура страницы с реквизитами карты"""
    keyboard = [
        [InlineKeyboardButton(text="📸 Отправить чек об оплате", callback_data=f"send_receipt:{product_key}")],
        [
            InlineKeyboardButton(text="⬅️ Назад к товару", callback_data=f"prod:{product_key}"),
            InlineKeyboardButton(text="🏠 Меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cancel_receipt_keyboard(product_key: str) -> InlineKeyboardMarkup:
    """Кнопка отмены отправки чека"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Отменить отправку чека", callback_data=f"prod:{product_key}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_receipt_keyboard(user_id: int, product_key: str) -> InlineKeyboardMarkup:
    """Кнопки проверки чека для администратора"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Одобрить и выдать", callback_data=f"adm_appr:{user_id}:{product_key}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"adm_decl:{user_id}:{product_key}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура панели администратора"""
    keyboard = [
        [InlineKeyboardButton(text="📊 Статистика и доходы", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Рассылка всем пользователям", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="📦 Товары и цены", callback_data="admin_products")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_back_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в админ-панель"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Назад в админку", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_cancel_broadcast_keyboard() -> InlineKeyboardMarkup:
    """Кнопка отмены рассылки"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Отменить рассылку", callback_data="admin_cancel_broadcast")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
