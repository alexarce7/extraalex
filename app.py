import web
# @
from web import form
from datos import Clientes
from datos import Peliculas
render=web.template.render('templates')
urls = (
    '/(.*)', 'index'
)

db = web.database(dbn='mysql', db='peliculas', user='root', pw='utec')

Clientes = Clientes()  
Clientes.read()
Peliculas=Peliculas()
Peliculas.read()
myform = form.Form( 
    form.Dropdown('Cliente', Clientes.getClientes()), 
    
    form.Dropdown('Pelicula',Peliculas.getPeliculas()), 
    form.Dropdown('Formato', ["Blueray","DVD"]),
    form.Textbox('Tiempo')
    
    ) 
class index:
    def GET(self,results):
        form = myform()
        resultado=db.select('peliculas')
        return render.index(form,resultado)
        
    def POST(self,results): 
        form = myform() 
        if not form.validates(): 
            return render.index(form)
        else:
            costo=0
            if form.d.Formato=="Blueray":
                costo=20
            elif form.d.Formato=="DVD":
                costo=10
            total=int(form.d.Tiempo)*costo
            db.insert('peliculas',pelicula=form.d.Pelicula, 
            formato=form.d.Formato,cliente=form.d.Cliente, 
            tiempo=form.d.Tiempo,total=total)
            
            resultado=db.select('peliculas')
           
            return render.index(form,resultado)
    

if __name__ == "__main__":
    
    app = web.application(urls, globals())
    app.run()