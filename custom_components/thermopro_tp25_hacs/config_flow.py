"""Config flow for TP25."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class TP25ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a TP25 config flow."""

    async def async_step_user(self, user_input: dict | None = None):
        """
        Docstring for async_step_user.

        :param self: Description
        :param user_input: Description
        :type user_input: dict | None
        """
        if user_input is not None:
            return self.async_create_entry(
                title="TP25 BLE",
                data={"address": user_input["address"]},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("address"): str},
            ),
        )
