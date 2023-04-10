from odoo import _
import base64
from odoo.http import *
from odoo.addons.website.controllers.main import QueryURL


class WebController(Controller):
    
    def convertir_filtro(self, filtro):
        aux = filtro.split(';')
        if aux[2] == 'None':
            aux[2] = None
        elif aux[2] == 'True':
            aux[2] = True
        elif aux[2] == 'False':
            aux[2] = False
        
        return tuple(aux)
    
    
    #ruta para la pagina de los donde aparecen los cursos.
    @route([
        '/cursos', 
        '/cursos/page/<int:page>',
    ], auth='public', website=True)
    def cursos(self, page=0, filterby='',order='', search='',**post):
        
        Cursos = request.env['openacademy.cursos'].with_context(bin_size=True)
       
        domain = []

        if order == '':
            order = 'titulo asc'
           
        if search != '' : 
            domain = [('titulo', 'ilike', search)]

        if filterby != '':
            domain.append(self.convertir_filtro(filterby))
        
        
        keep = QueryURL('/cursos', search=search, filterby=filterby, order=order)
        
      
        post['order'] = order
        post["search"] = search
        post["filterby"] = filterby
           

        pager = request.website.pager(
        url='/cursos',
        total=Cursos.sudo().search_count(domain),
        page=page,
        step=3,
        url_args=post
        )
        

        object_value = Cursos.sudo().search(domain,order=order)
        offset = pager['offset']
    
        
        values = {
            'records' : object_value[offset: offset + 3],
            'order' : post.get('order'),
            'pager' : pager,
            'search': search,
            'keep': keep,
            }
       
        return request.render('webcontroller_open_academy.cursos_template', values)
    
    
    #ruta para la pagina donde aparecen las sesiones de un curso en especifico.
    @route(['/cursos/<int:curso_id>/sesiones','/cursos/<int:curso_id>/sesiones/page/<int:page>'], auth='public', website=True)
    def sesiones(self, curso_id, page=0):
        pager = request.website.pager(
        url='/cursos/{0}/sesiones'.format(curso_id),
        total=request.env['openacademy.sesiones'].sudo().search_count([('curso_id', '=', int(curso_id))]),
        page=page,
        step=3,
        )
        
        object_value = request.env['openacademy.sesiones'].sudo().search([('curso_id', '=', int(curso_id))])
        
        offset = pager['offset']

        values = {
            'records' : object_value[offset: offset + 3] ,
            'titulo_curso' : request.env['openacademy.cursos'].sudo().search([('id', '=', int(curso_id))])[0].titulo,
            'pager' : pager,
            'user' : request.env.user.partner_id,
            'curso_id' : curso_id,

        }
        return request.render('webcontroller_open_academy.sesiones_template', values)

    #ruta para la pagina donde aparecen la confirmación de la asistencia de una sesión.
    @route([
        '/curso/<int:curso_id>/sesion/<int:sesion_id>/user/<int:user_id>/add',
        '/curso/<int:curso_id>/sesion/<int:sesion_id>/user/<int:user_id>/add/<string:detalles>'
    ], type="http" ,auth='user', website=True)
    def add_asistente(self,curso_id ,sesion_id, user_id,detalles = ""):
        user = request.env['res.partner'].sudo().browse(user_id)
        request.env['openacademy.sesiones'].sudo().browse(sesion_id).update({'asistentes_ids' : [(4,user.id)]})
        values = {
            'curso_id' : curso_id,
            'titulo_curso' : request.env['openacademy.cursos'].sudo().browse(curso_id).titulo,
            'detalles': True if detalles == "detalles" else False,
            'sesion_id' : sesion_id,
            
            }
        return request.render('webcontroller_open_academy.sesiones_template_confirm',values)
    
    #ruta para la pagina donde aparecen la confirmación de la eliminación de una asistencia en una sesión.
    @route([
        "/curso/<int:curso_id>/sesion/<int:sesion_id>/user/<int:user_id>/delete",
        '/curso/<int:curso_id>/sesion/<int:sesion_id>/user/<int:user_id>/delete/<string:detalles>'
        ], type="http" ,auth='user', website=True)
    def delete_asistente(self,curso_id ,sesion_id, user_id, detalles = ""):
        request.env['openacademy.sesiones'].sudo().browse(sesion_id).write({
            'asistentes_ids' :  [(3, user_id)]
        })
        values = {
            'curso_id' : curso_id,
            'titulo_curso' : request.env['openacademy.cursos'].sudo().browse(curso_id).titulo,
            'detalles': True if detalles == "detalles" else False,
            'sesion_id' : sesion_id,
        }
        return request.render('webcontroller_open_academy.sesiones_template_delete',values)

    #ruta de la cuál se descargan los archivos adjuntos a los cursos.
    @route(['/documentos/<int:doc_id>/download'], type="http", auth='public')
    def download(self,doc_id):
        Doc = request.env['ir.attachment'].sudo().browse(doc_id)
        data = Doc.datas and Doc.datas.decode() or ''
        file = base64.b64decode(data)

        headers = [
            ('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition(Doc.name)),
            ]
        return request.make_response(file, headers=headers)
    

    #ruta para la pagina donde aparece la información completa de un curso especifico.
    @route(["/curso/<int:curso_id>/complete"], type="http", auth='public', website=True)
    def cursos_completo(self,curso_id):
        values = {
            'curso' : request.env['openacademy.cursos'].sudo().browse(curso_id),
        }    
        return request.render('webcontroller_open_academy.curso_completo', values)
    
    #ruta para la pagina donde aparece la información completa de una sesión especifica.
    @route(["/curso/<int:curso_id>/sesiones/<int:sesion_id>/complete"], type="http", auth='public', website=True)
    def sesiones_completo(self,curso_id,sesion_id):
        values = {
            'curso' : request.env['openacademy.cursos'].sudo().browse(curso_id),
            'sesion': request.env['openacademy.sesiones'].sudo().browse(sesion_id),
            'user' : request.env.user.partner_id,
        }    
        return request.render('webcontroller_open_academy.sesiones_completas', values)
