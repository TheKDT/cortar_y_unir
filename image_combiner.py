from PIL import Image
import os
import re

def natural_sort_key(s):
    """
    Clave de ordenamiento natural para usar con sorted(), para ordenar alfanuméricamente.
    Extrae todos los números y los trata como valores enteros durante el ordenamiento.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def get_unique_filename(directory, base_name, extension, part_suffix=""):
    """
    Crea un nombre de archivo único en el directorio dado.
    Si el archivo ya existe, añade un contador al nombre del archivo hasta que sea único.
    """
    counter = 1
    filename = f"{base_name}{part_suffix}.{extension}"
    file_path = os.path.join(directory, filename)
    while os.path.exists(file_path):
        filename = f"{base_name}{part_suffix}_{counter}.{extension}"
        file_path = os.path.join(directory, filename)
        counter += 1
    return file_path

def combine_images(folder_path, output_format='JPEG', output_directory=None):
    """
    Combina todas las imágenes en un directorio en una sola imagen verticalmente.
    Si la altura combinada excede el máximo permitido, la imagen se divide en múltiples partes.
    """
    if output_directory is None:
        output_directory = folder_path

    # Lista de imágenes a combinar
    images = [Image.open(os.path.join(folder_path, img)) for img in sorted(os.listdir(folder_path), key=natural_sort_key) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        return  # Termina la función si no hay imágenes para combinar

    # Determina el ancho máximo para la imagen combinada
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    
    total_height = 0
    part_number = 1
    new_im = Image.new('RGB', (max_width, 65500))
    y_offset = 0
    
    # Itera sobre cada imagen y pégala en la imagen combinada
    for im in images:
        if y_offset + im.height > 65500:
            output_file_path = get_unique_filename(output_directory, "combined_image_part", output_format.lower(), f"{part_number}")
            new_im = new_im.crop((0, 0, max_width, y_offset))
            new_im.save(output_file_path, output_format, quality=95)
            part_number += 1
            new_im = Image.new('RGB', (max_width, 65500))
            y_offset = 0
        
        new_im.paste(im, (0, y_offset))
        y_offset += im.height

    # Guarda la última parte de la imagen combinada
    if y_offset > 0:
        output_file_path = get_unique_filename(output_directory, "combined_image_part", output_format.lower(), f"{part_number}")
        new_im = new_im.crop((0, 0, max_width, y_offset))
        new_im.save(output_file_path, output_format, quality=95)

def get_filename_for_replacement(directory, base_name, extension, part_suffix=""):
    """
    Construye un nombre de archivo con un sufijo opcional.
    Esta función se utiliza cuando se desea reemplazar una imagen existente o guardar una nueva.
    """
    filename = f"{base_name}{part_suffix}.{extension}"
    file_path = os.path.join(directory, filename)
    return file_path

def process_image(image_path, output_directory, parts):
    """
    Divide una imagen en varias partes y las guarda individualmente.
    """
    image = Image.open(image_path)
    width, height = image.size
    part_height = height // parts

    # Corta la imagen en la cantidad especificada de partes y guarda cada parte
    for i in range(parts):
        start_height = i * part_height
        end_height = (i + 1) * part_height if i < parts - 1 else height
        part_image = image.crop((0, start_height, width, end_height))
        output_path = get_filename_for_replacement(output_directory, os.path.splitext(os.path.basename(image_path))[0], "jpg", f"_part{i+1}")
        part_image.save(output_path, "JPEG", quality=95)

def cut_images(folder_path, parts, output_directory):
    """
    Procesa múltiples imágenes en un directorio, dividiéndolas en el número especificado de partes.
    """
    # Itera sobre los archivos de imagen en el directorio y los procesa individualmente
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file_name)
            process_image(image_path, output_directory, parts)
