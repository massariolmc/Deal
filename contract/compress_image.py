from io import BytesIO
from PIL import Image
from django.core.files import File

#Deleta as imagens em um update, caso não sejam iguais
def delete_old_image(Model,pk, image):
    marc = 0   
    if pk:
        c = Model.objects.get(id=pk)        
        if c.image != image:            
            c.image.delete(save=False)# O padrão é true se for deletar tudo. Se for deletar só a imagem ou arquivo é false 
            marc = 1            
    return marc      

#Comprime imagens
def compress(image):
    im = Image.open(image)
    # Converte se a imagem não for um JPEG. Arquivo JPEG são RGB.
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=70) 
    # create a Django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image