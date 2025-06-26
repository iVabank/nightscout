"""Сервис для отправки данных глюкозы на Алису Макс."""
from __future__ import annotations

import logging
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.components.notify import ATTR_MESSAGE, ATTR_TARGET

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nightscout_mmol"
SERVICE_SEND_TO_ALICE = "send_to_alice"

ALICE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional(ATTR_TARGET): cv.string,  # ID устройства (если несколько колонок)
    }
)

async def async_setup_services(hass: HomeAssistant) -> None:
    """Регистрация сервиса."""
    async def send_to_alice(call: ServiceCall) -> None:
        """Отправка сообщения на Алису."""
        message = call.data[ATTR_MESSAGE]
        target = call.data.get(ATTR_TARGET)  # Опционально: конкретная колонка

        # Используем стандартный сервис notify.yandex_station (если он есть)
        await hass.services.async_call(
            "notify",
            "yandex_station",  # или ваш кастомный notify-сервис для Алисы
            {"message": message, "target": target} if target else {"message": message},
            blocking=True,
        )

    hass.services.async_register(
        DOMAIN, SERVICE_SEND_TO_ALICE, send_to_alice, schema=ALICE_SCHEMA
    )

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Добавляем сервис при загрузке интеграции."""
    await async_setup_services(hass)
    return True