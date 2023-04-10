from odoo.http import *
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo import _
from odoo.exceptions import AccessError, MissingError

class OpenAcademyPortal(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = ('asistentes_ids', '=', request.env.user.partner_id.id)
        if 'sesion_count' in counters:
            values['sesion_count'] = request.env['openacademy.sesiones'].search_count([domain]) \
            if request.env['openacademy.sesiones'].check_access_rights('read', raise_exception=False) else 0
        return values
    

    def _sesion_get_page_view_values(self, sesiones, access_token, **kwargs):
        values = {
            'page_name': 'sesiones',
            'sesion': sesiones,
        }
        return self._get_page_view_values(sesiones, access_token, values, 'my_sesiones_history', False, **kwargs)


    @route(['/my/sesiones', '/my/sesiones/page/<int:page>'], auth="user", website=True)
    def portal_my_sesiones(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Sesiones = request.env['openacademy.sesiones']
        domain = [('asistentes_ids', '=', request.env.user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'nombre'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # sesiones count
        sesiones_count = Sesiones.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/sesiones",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=sesiones_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        sesiones = Sesiones.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_sesiones_history'] = sesiones.ids[:100]
        
        Cursos = []

        for sesion in sesiones:
            if sesion.curso_id  not in Cursos:
                Cursos.append(sesion.curso_id)
        

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'sesiones': sesiones,
            'page_name': 'sesiones',
            'default_url': '/my/sesiones',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'cursos': Cursos,
        })
        return request.render("webcontroller_open_academy.portal_my_sesiones", values)
    
    @route(['/my/sesion/<int:sesion_id>'], type='http', auth="user", website=True)
    def portal_my_sesion(self, sesion_id=None, access_token=None, **kw):
        try:
            sesion_sudo = self._document_check_access('openacademy.sesiones', sesion_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        for attachment in sesion_sudo.attachment_ids:
            attachment.generate_access_token()
    
        values = self._sesion_get_page_view_values(sesion_sudo, access_token, **kw)
        values.update({
            'curso_id': sesion_sudo.curso_id.id,
            'user': request.env.user.partner_id
        })
        return request.render("webcontroller_open_academy.portal_my_sesion", values)


