from typing import Dict, Tuple, Union
from urllib.parse import quote

import aiohttp
from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django_nextjs.render import (
    _get_nextjs_request_cookies, _get_nextjs_response_headers,
    _get_nextjs_request_headers, _get_render_context)


async def _render_nextjs_page_to_string(
    request: HttpRequest,
    template_name: str = "",
    context: Union[Dict, None] = None,
    using: Union[str, None] = None,
    allow_redirects: bool = False,
    headers: Union[Dict, None] = None,
    schema: str = "public"
) -> Tuple[str, int, Dict[str, str]]:
    page_path = quote(request.path_info.lstrip("/"))
    params = [(k, v) for k in request.GET.keys()
              for v in request.GET.getlist(k)]
    params.append(('schema', 'pasal'))

    async with aiohttp.ClientSession(
        cookies=_get_nextjs_request_cookies(request),
        headers=_get_nextjs_request_headers(request, headers),
    ) as session:
        async with session.get(
            f"http://{schema}.localhost:3000/{page_path}", params=params,
            allow_redirects=allow_redirects
        ) as response:
            html = await response.text()
            response_headers = _get_nextjs_response_headers(response.headers)
    if template_name:
        render_context = _get_render_context(html, context)
        if render_context is not None:
            html = await sync_to_async(render_to_string)(
                template_name, context=render_context,
                request=request, using=using
            )
    return html, response.status, response_headers


async def render_nextjs_page(
    request: HttpRequest,
    template_name: str = "",
    context: Union[Dict, None] = None,
    using: Union[str, None] = None,
    allow_redirects: bool = False,
    headers: Union[Dict, None] = None,
    schema: str = 'public',
):
    content, status, response_headers = await _render_nextjs_page_to_string(
        request,
        template_name,
        context,
        using=using,
        allow_redirects=allow_redirects,
        headers=headers,
        schema=schema,
    )
    return HttpResponse(content=content, status=status,
                        headers=response_headers)


async def index(request):
    return await render_nextjs_page(request, schema='pasal')
