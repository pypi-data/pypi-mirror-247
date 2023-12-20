from typing import Any, Dict, List, Optional

import aiohttp

from .utils import _to_json
from .exceptions import HTTPException, NotFound, DataConflict

__all__ = ("HTTPClient", )


class HTTPClient:
    def __init__(self, api_url: str, token: str) -> None:
        self.api_url = api_url
        self.session = aiohttp.ClientSession(headers={"User-Agent": "Sanctum-TC (https://github.com/lightning-bot/sanctum-tc.git)",
                                                      "X-API-Key": token})

    async def close(self):
        """Closes the client session"""
        await self.session.close()

    async def request(self, method: str, path: str, **kwargs) -> dict:
        """Makes a request to the API.

        Parameters
        ----------
        method : str
            The method to use to send a request to the route. GET, PUT, POST, DELETE
        path : str
            The path to send the request to.
        """
        url = self.api_url + path

        if data := kwargs.pop("data", None):
            kwargs['headers'] = {'Content-Type': 'application/json'}
            kwargs['data'] = _to_json(data)

        async with self.session.request(method, url, **kwargs) as resp:
            data = await resp.json()
            if 300 > resp.status >= 200:
                return data

            if resp.status == 404:
                raise NotFound(resp.status, data)

            if resp.status == 409:
                raise DataConflict(resp.status, data)

            raise HTTPException(resp.status, data)

    # Guild state management

    async def get_guild(self, guild_id: int):
        return await self.request("GET", f"/guilds/{guild_id}")

    async def create_guild(self, guild_id: int, payload: dict):
        return await self.request("PUT", f"/guilds/{guild_id}", data=payload)

    async def update_guild(self, guild_id: int, payload: dict):
        return await self.create_guild(guild_id, payload)

    async def leave_guild(self, guild_id: int):
        return await self.request("DELETE", f"/guilds/{guild_id}/leave")

    # Timer management

    async def create_timer(self, payload: dict):
        return await self.request("PUT", "/timers", data=payload)

    async def delete_timer(self, id: int):
        return await self.request("DELETE", f"/timers/{id}")

    async def get_timer(self, id: int):
        return await self.request("GET", f"/timers/{id}")

    async def get_timers(self, *, limit: int = 1):
        return await self.request("GET", "/timers", params={"limit": str(limit)})

    async def get_user_reminder(self, user_id: int, reminder_id: int):
        return await self.request("GET", f"/users/{user_id}/reminders/{reminder_id}")

    async def get_user_reminders(self, user_id: int, *, limit: int = 10):
        return await self.request("GET", f"/users/{user_id}/reminders", params={"limit": str(limit)})

    async def delete_user_reminder(self, user_id: int, reminder_id: int):
        return await self.request("DELETE", f"/users/{user_id}/reminders/{reminder_id}")

    # Infraction management

    async def create_infraction(self, guild_id: int, payload: dict):
        return await self.request("PUT", f"/guilds/{guild_id}/infractions", data=payload)

    async def get_infraction(self, guild_id: int, infraction_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/infractions/{infraction_id}")

    async def get_infractions(self, guild_id: int,
                              action_num: Optional[int] = None):
        params = {}
        if action_num is not None:
            params['action'] = action_num

        return await self.request("GET", f"/guilds/{guild_id}/infractions",
                                  params=params)

    async def delete_infraction(self, guild_id: int, infraction_id: int):
        return await self.request("DELETE", f"/guilds/{guild_id}/infractions/{infraction_id}")

    async def edit_infraction(self, guild_id: int, infraction_id: int, payload: dict):
        return await self.request("PATCH", f"/guilds/{guild_id}/infractions/{infraction_id}", data=payload)

    async def bulk_delete_user_infractions(self, guild_id: int, user_id: int):
        return await self.request("DELETE", f"/guilds/{guild_id}/users/{user_id}/infractions")

    async def get_user_infractions(self, guild_id, user_id: int, *,
                                   action_num: Optional[int] = None):
        params = {}
        if action_num is not None:
            params['action'] = action_num

        return await self.request("GET", f"/guilds/{guild_id}/users/{user_id}/infractions", params=params)

    # Configuration
    async def get_guild_bot_config(self, guild_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/config")

    async def bulk_upsert_guild_prefixes(self, guild_id: int, prefixes: List[str]):
        return await self.request("PUT", f"/guilds/{guild_id}/prefixes", data=prefixes)

    async def get_guild_moderation_config(self, guild_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/config/moderation")

    # Pastes
    async def create_paste(self, text: str):
        return await self.request("PUT", "/admin/paste", data={'text': text})

    async def delete_paste(self, url: str):
        return await self.request("DELETE", "/admin/paste", params={'url': url})

    # AutoMod
    async def get_guild_automod_config(self, guild_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/automod")

    async def bulk_upsert_guild_automod_default_ignores(self, guild_id: int, ignores: List[int]):
        return await self.request("PUT", f"/guilds/{guild_id}/automod/ignores", data=ignores)

    async def get_guild_automod_rules(self, guild_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/automod/rules")

    async def create_guild_automod_rule(self, guild_id: int, payload: Dict[str, Any]):
        return await self.request("PUT", f"/guilds/{guild_id}/automod/rules", data=payload)

    async def delete_guild_automod_rule(self, guild_id: int, rule: str):
        return await self.request("DELETE", f"/guilds/{guild_id}/automod/rules/{rule}")

    # Message Reports
    async def get_guild_message_report(self, guild_id: int, message_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/reports/{message_id}")

    async def create_guild_message_report(self, guild_id: int, payload: Dict[str, Any]):
        return await self.request("PUT", f"/guilds/{guild_id}/reports", data=payload)

    async def add_guild_message_reporter(self, guild_id: int, message_id: int, payload: Dict[str, Any]):
        return await self.request("PUT", f"/guilds/{guild_id}/reports/{message_id}/reporters", data=payload)

    async def get_guild_message_reporters(self, guild_id: int, message_id: int):
        return await self.request("GET", f"/guilds/{guild_id}/reports/{message_id}/reporters")

    async def edit_guild_message_report(self, guild_id: int, message_id: int, payload: Dict[str, Any]):
        return await self.request("PATCH", f"/guilds/{guild_id}/reports/{message_id}", data=payload)
