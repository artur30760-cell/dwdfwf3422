import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    PreCheckoutQuery,
    LabeledPrice
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from config import (
    BOT_TOKEN,
    OWNER_ID,
    PRODUCTS,
    SUPPORT_USERNAME,
    PROXY,
    BANK_NAME,
    CARD_NUMBER,
    CARD_HOLDER
)

from keyboards import (
    main_menu_keyboard,
    catalog_keyboard,
    product_detail_keyboard,
    card_payment_keyboard,
    cancel_receipt_keyboard,
    admin_receipt_keyboard,
    admin_menu_keyboard,
    admin_back_keyboard,
    admin_cancel_broadcast_keyboard
)
from database import (
    init_db,
    add_user,
    add_order,
    get_stats,
    get_all_user_ids
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация сессии и бота
session = AiohttpSession(proxy=PROXY) if PROXY else None
bot = Bot(
    token=BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Состояния для FSM
class UserStates(StatesGroup):
    waiting_for_receipt = State()


class AdminStates(StatesGroup):
    waiting_for_broadcast_message = State()


WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в магазин промтов!</b>\n\n"
    "Здесь вы можете приобрести готовые промты и инструкции для популярных нейросетей.\n\n"
    "💳 <b>Способы оплаты:</b>\n"
    "• ⭐️ Telegram Stars (Звёзды) — моментальная выдача\n"
    "• 💳 Перевод на карту (Рубли) — по чеку\n\n"
    "Выберите нужное действие в меню ниже:"
)


# ================== ОБЩИЕ ХЭНДЛЕРЫ ==================

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()
    user = message.from_user
    add_user(user.id, user.username or "", user.full_name)
    is_admin = (user.id == OWNER_ID)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard(is_admin=is_admin))


@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    user = callback.from_user
    add_user(user.id, user.username or "", user.full_name)
    is_admin = (user.id == OWNER_ID)
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_keyboard(is_admin=is_admin))
    await callback.answer()


@dp.callback_query(F.data == "catalog")
async def cb_catalog(callback: CallbackQuery, state: FSMContext):
    """Отображение каталога товаров"""
    await state.clear()
    text = (
        "🛍 <b>Каталог промтов</b>\n\n"
        "Выберите интересующую нейросеть, чтобы ознакомиться с описанием и перейти к покупке:"
    )
    await callback.message.edit_text(text, reply_markup=catalog_keyboard())
    await callback.answer()


@dp.callback_query(F.data.startswith("prod:"))
async def cb_product_detail(callback: CallbackQuery, state: FSMContext):
    """Просмотр карточки товара"""
    await state.clear()
    product_key = callback.data.split("prod:")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    text = (
        f"📦 <b>{product['name']}</b>\n\n"
        f"📝 <b>Описание:</b>\n{product['description']}\n\n"
        f"💰 <b>Стоимость:</b>\n"
        f"• 💳 Рублями: <b>{product['price_rub']} ₽</b>\n"
        f"• ⭐️ Звёздами: <b>{product['price_stars']} ⭐️</b>\n\n"
        f"<i>Выберите удобный способ оплаты ниже:</i>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=product_detail_keyboard(product_key, product["price_stars"], product["price_rub"])
    )
    await callback.answer()


# ================== ОПЛАТА ЗВЁЗДАМИ ==================

@dp.callback_query(F.data.startswith("buy_stars:"))
async def cb_buy_stars(callback: CallbackQuery):
    """Отправка инвойса на оплату звёздами"""
    product_key = callback.data.split("buy_stars:")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    await callback.answer()
    
    await callback.message.answer_invoice(
        title=f"Промт: {product['name']}",
        description=f"Покупка промта и инструкции для {product['name']}",
        payload=product_key,
        currency="XTR",  # Код Telegram Stars
        prices=[
            LabeledPrice(label=product["name"], amount=product["price_stars"])
        ],
        provider_token=""  # Для звёзд токен пустой
    )


@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Подтверждение готовности принять платеж звёздами"""
    product_key = pre_checkout_query.invoice_payload
    if product_key in PRODUCTS:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False, error_message="Товар больше недоступен.")


@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Обработка успешной оплаты звёздами и выдача товара"""
    payment = message.successful_payment
    product_key = payment.invoice_payload
    stars_paid = payment.total_amount
    product = PRODUCTS.get(product_key)

    # Сохраняем заказ в базу данных
    add_order(message.from_user.id, product_key, stars_paid, currency="XTR")

    if not product:
        await message.answer(
            "⚠️ Оплата прошла, но возникла ошибка при поиске товара.\n"
            f"Пожалуйста, свяжитесь с поддержкой: @{SUPPORT_USERNAME}"
        )
        return

    response_text = (
        f"✅ <b>Оплата успешно принята!</b> (Списано: {stars_paid} ⭐️)\n\n"
        f"{product['content']}"
    )

    is_admin = (message.from_user.id == OWNER_ID)
    await message.answer(response_text, reply_markup=main_menu_keyboard(is_admin=is_admin), disable_web_page_preview=True)


    # Уведомление владельца
    if OWNER_ID:
        try:
            buyer_user = message.from_user
            buyer_mention = f"@{buyer_user.username}" if buyer_user.username else f"ID: {buyer_user.id}"
            admin_notify_text = (
                f"🔔 <b>Новая покупка (Звёзды)!</b>\n\n"
                f"👤 Покупатель: {buyer_mention} ({buyer_user.full_name})\n"
                f"📦 Товар: <b>{product['name']}</b>\n"
                f"💰 Сумма: {stars_paid} ⭐️"
            )
            await bot.send_message(chat_id=OWNER_ID, text=admin_notify_text)
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление владельцу: {e}")


# ================== ОПЛАТА НА КАРТУ (РУБЛИ) ==================

@dp.callback_query(F.data.startswith("buy_card:"))
async def cb_buy_card(callback: CallbackQuery):
    """Показ реквизитов карты для перевода"""
    product_key = callback.data.split("buy_card:")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    text = (
        f"💳 <b>Оплата переводом на карту</b>\n\n"
        f"📦 <b>Товар:</b> {product['name']}\n"
        f"💰 <b>Сумма к переводу:</b> <code>{product['price_rub']}</code> ₽\n\n"
        f"🏦 <b>Банк:</b> <b>{BANK_NAME}</b>\n"
        f"💳 <b>Номер карты:</b>\n<code>{CARD_NUMBER}</code> <i>(нажмите, чтобы скопировать)</i>\n\n"
        f"👤 <b>Получатель:</b> {CARD_HOLDER}\n\n"
        f"⚠️ <b>Инструкция:</b>\n"
        f"1. Переведите точную сумму <b>{product['price_rub']} ₽</b> на карту <b>{BANK_NAME}</b>.\n"
        f"2. Сохраните чек/скриншот перевода.\n"
        f"3. Нажмите кнопку <b>«📸 Отправить чек об оплате»</b> ниже и отправьте фото чека.\n\n"
        f"🌙 <i>Примечание: если вы оплачиваете ночью, проверка может занять несколько часов (до утра).</i>"
    )

    await callback.message.edit_text(text, reply_markup=card_payment_keyboard(product_key))
    await callback.answer()


@dp.callback_query(F.data.startswith("send_receipt:"))
async def cb_start_send_receipt(callback: CallbackQuery, state: FSMContext):
    """Запрос отправки фото чека"""
    product_key = callback.data.split("send_receipt:")[1]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    await state.set_state(UserStates.waiting_for_receipt)
    await state.update_data(product_key=product_key)

    text = (
        f"📸 <b>Отправка чека</b>\n\n"
        f"Товар: <b>{product['name']}</b> ({product['price_rub']} ₽)\n\n"
        f"Пожалуйста, отправьте <b>фотографию, скриншот или документ</b> с чеком об оплате:"
    )
    await callback.message.edit_text(text, reply_markup=cancel_receipt_keyboard(product_key))
    await callback.answer()


@dp.message(UserStates.waiting_for_receipt, F.photo | F.document)
async def process_receipt_message(message: Message, state: FSMContext):
    """Обработка присланного чека и пересылка владельцу"""
    data = await state.get_data()
    product_key = data.get("product_key")
    product = PRODUCTS.get(product_key)

    if not product:
        await message.answer("Ошибка: товар не найден. Попробуйте снова через каталог.")
        await state.clear()
        return

    await state.clear()
    buyer = message.from_user
    buyer_mention = f"@{buyer.username}" if buyer.username else f"ID: {buyer.id}"

    # Сообщение покупателю
    await message.answer(
        "⏳ <b>Чек успешно отправлен на проверку!</b>\n\n"
        "Администратор проверит поступление средств в ближайшее время. "
        "После одобрения бот автоматически пришлет вам купленный промт и инструкцию сюда.\n\n"
        "🌙 <i>Примечание: если вы оплачиваете ночью, пожалуйста, учтите, что скорее всего придется подождать несколько часов.</i>",
        reply_markup=main_menu_keyboard(is_admin=(buyer.id == OWNER_ID))
    )


    # Пересылка владельцу
    admin_caption = (
        f"🔔 <b>Новый чек на проверку!</b>\n\n"
        f"👤 Покупатель: {buyer_mention} ({buyer.full_name})\n"
        f"🆔 ID покупателя: <code>{buyer.id}</code>\n"
        f"📦 Товар: <b>{product['name']}</b>\n"
        f"💰 Ожидаемая сумма: <b>{product['price_rub']} ₽</b>"
    )

    try:
        if message.photo:
            # Отправляем фото
            photo_file_id = message.photo[-1].file_id
            await bot.send_photo(
                chat_id=OWNER_ID,
                photo=photo_file_id,
                caption=admin_caption,
                reply_markup=admin_receipt_keyboard(buyer.id, product_key)
            )
        elif message.document:
            # Отправляем документ
            await bot.send_document(
                chat_id=OWNER_ID,
                document=message.document.file_id,
                caption=admin_caption,
                reply_markup=admin_receipt_keyboard(buyer.id, product_key)
            )
    except Exception as e:
        logger.error(f"Не удалось отправить чек владельцу: {e}")


@dp.message(UserStates.waiting_for_receipt)
async def process_invalid_receipt(message: Message):
    """Если пользователь отправил не фото/документ"""
    await message.answer("⚠️ Пожалуйста, отправьте именно **скриншот или фото чека** (изображением или файлом).")


# ================== ОБРАБОТКА ЧЕКОВ АДМИНИСТРАТОРОМ ==================

@dp.callback_query(F.data.startswith("adm_appr:"))
async def cb_admin_approve_receipt(callback: CallbackQuery):
    """Одобрение чека администратором и выдача товара"""
    if callback.from_user.id != OWNER_ID:
        return

    parts = callback.data.split(":")
    buyer_id = int(parts[1])
    product_key = parts[2]
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    # Записываем заказ в БД
    add_order(buyer_id, product_key, product["price_rub"], currency="RUB")

    # Обновляем сообщение у админа
    new_caption = f"{callback.message.caption or callback.message.text}\n\n✅ <b>ОДОБРЕНО</b> — товар выдан покупателю."
    if callback.message.photo or callback.message.document:
        await callback.message.edit_caption(caption=new_caption, reply_markup=None)
    else:
        await callback.message.edit_text(text=new_caption, reply_markup=None)

    await callback.answer("Заказ одобрен! Товар отправлен.")

    # Отправляем товар покупателю
    delivery_text = (
        f"✅ <b>Ваш платёж на сумму {product['price_rub']} ₽ подтверждён!</b>\n\n"
        f"{product['content']}"
    )
    try:
        await bot.send_message(
            chat_id=buyer_id,
            text=delivery_text,
            reply_markup=main_menu_keyboard(is_admin=(buyer_id == OWNER_ID)),
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Не удалось доставить товар покупателю {buyer_id}: {e}")



@dp.callback_query(F.data.startswith("adm_decl:"))
async def cb_admin_decline_receipt(callback: CallbackQuery):
    """Отклонение чека администратором"""
    if callback.from_user.id != OWNER_ID:
        return

    parts = callback.data.split(":")
    buyer_id = int(parts[1])
    product_key = parts[2]
    product = PRODUCTS.get(product_key)
    p_name = product['name'] if product else product_key

    # Обновляем сообщение у админа
    new_caption = f"{callback.message.caption or callback.message.text}\n\n❌ <b>ОТКЛОНЕНО</b> администратором."
    if callback.message.photo or callback.message.document:
        await callback.message.edit_caption(caption=new_caption, reply_markup=None)
    else:
        await callback.message.edit_text(text=new_caption, reply_markup=None)

    await callback.answer("Чек отклонён.")

    # Уведомляем покупателя
    decline_text = (
        f"❌ <b>Ваш чек по товару «{p_name}» был отклонён администратором.</b>\n\n"
        f"Возможные причины: средства не поступили, неверная сумма или нечитаемый чек.\n"
        f"Если вы совершили оплату, пожалуйста, напишите в поддержку: @{SUPPORT_USERNAME}"
    )
    try:
        await bot.send_message(
            chat_id=buyer_id,
            text=decline_text,
            reply_markup=main_menu_keyboard(is_admin=(buyer_id == OWNER_ID))
        )
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление покупателю {buyer_id}: {e}")


# ================== АДМИН-ПАНЕЛЬ ==================

@dp.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    """Команда /admin для входа в панель администратора"""
    if message.from_user.id != OWNER_ID:
        return
    await state.clear()
    await message.answer(
        "👑 <b>Панель администратора</b>\n\nВыберите нужный раздел:",
        reply_markup=admin_menu_keyboard()
    )


@dp.callback_query(F.data == "admin_panel")
async def cb_admin_panel(callback: CallbackQuery, state: FSMContext):
    """Вход в панель администратора через кнопку"""
    if callback.from_user.id != OWNER_ID:
        await callback.answer("У вас нет доступа.", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(
        "👑 <b>Панель администратора</b>\n\nВыберите нужный раздел:",
        reply_markup=admin_menu_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "admin_stats")
async def cb_admin_stats(callback: CallbackQuery):
    """Просмотр статистики"""
    if callback.from_user.id != OWNER_ID:
        return
    
    stats = get_stats()
    text = (
        "📊 <b>Статистика магазина:</b>\n\n"
        f"👥 Всего пользователей: <b>{stats['total_users']}</b>\n"
        f"📦 Успешных покупок: <b>{stats['total_orders']}</b>\n\n"
        f"💰 <b>Заработано:</b>\n"
        f"• Рублями: <b>{stats['total_rubles']} ₽</b>\n"
        f"• Звёздами: <b>{stats['total_stars']} ⭐️</b>\n\n"
    )

    if stats["recent_orders"]:
        text += "<b>Последние покупки:</b>\n"
        for user_id, prod_key, amount, currency, created_at in stats["recent_orders"]:
            p_name = PRODUCTS.get(prod_key, {}).get("name", prod_key)
            curr_symbol = "⭐️" if currency == "XTR" else "₽"
            text += f"• <code>{user_id}</code> | {p_name} | {amount} {curr_symbol} | {created_at}\n"
    else:
        text += "<i>Покупок пока не было.</i>"

    await callback.message.edit_text(text, reply_markup=admin_back_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "admin_products")
async def cb_admin_products(callback: CallbackQuery):
    """Просмотр списка товаров и текущих цен"""
    if callback.from_user.id != OWNER_ID:
        return

    text = "📦 <b>Список товаров и цены:</b>\n\n"
    for key, item in PRODUCTS.items():
        text += (
            f"• <b>{item['name']}</b>\n"
            f"  Цена: <b>{item['price_rub']} ₽</b> / <b>{item['price_stars']} ⭐️</b>\n\n"
        )

    text += "<i>Чтобы изменить цены или тексты, отредактируйте файл config.py</i>"

    await callback.message.edit_text(text, reply_markup=admin_back_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "admin_broadcast")
async def cb_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    """Запуск процесса рассылки"""
    if callback.from_user.id != OWNER_ID:
        return

    await state.set_state(AdminStates.waiting_for_broadcast_message)
    text = (
        "📢 <b>Рассылка сообщений</b>\n\n"
        "Отправьте сообщение (текст, фото, видео или пересланный пост), "
        "которое нужно разослать всем пользователям бота."
    )
    await callback.message.edit_text(text, reply_markup=admin_cancel_broadcast_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "admin_cancel_broadcast")
async def cb_admin_cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    """Отмена рассылки"""
    if callback.from_user.id != OWNER_ID:
        return

    await state.clear()
    await callback.message.edit_text(
        "❌ Рассылка отменена.\n\n👑 <b>Панель администратора</b>",
        reply_markup=admin_menu_keyboard()
    )
    await callback.answer()


@dp.message(AdminStates.waiting_for_broadcast_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    """Отправка сообщения всем пользователям"""
    if message.from_user.id != OWNER_ID:
        return

    await state.clear()
    user_ids = get_all_user_ids()
    total_users = len(user_ids)

    if total_users == 0:
        await message.answer("В базе данных пока нет пользователей.", reply_markup=admin_menu_keyboard())
        return

    status_msg = await message.answer(f"⏳ Начинаю рассылку для {total_users} пользователей...")
    
    success_count = 0
    blocked_count = 0

    for uid in user_ids:
        try:
            await message.copy_to(chat_id=uid)
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            blocked_count += 1

    await status_msg.edit_text(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"👥 Всего пользователей: <b>{total_users}</b>\n"
        f"🟢 Успешно доставлено: <b>{success_count}</b>\n"
        f"🔴 Заблокировали бота/ошибки: <b>{blocked_count}</b>",
        reply_markup=admin_menu_keyboard()
    )


# ================== ЗАПУСК ==================

async def main():
    logger.info("Инициализация базы данных...")
    init_db()
    
    logger.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
