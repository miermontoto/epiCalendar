from posix import replace
import re

__version__ = "2.3"

EPI_CODE = '02.01'
EPM_CODE = '03.01'

EPI_BUILDING_CODES = {  # building codes for 'Milla del Conocimiento' (Gijón 02.01) sourced from gis.uniovi.es
    '01': 'AN',
    '02': 'AS',
    '04': 'DE',
    '05': 'DO',
    '08': 'EP'
}


def _parse_epi_location(name, code, building, floor) -> str:
    # Aula AS-1 through Aula AS-11
    result = re.search(r'02.01.02.00.P1.00.(0[1-9]|1[0-1])', code)
    if bool(result):
        return f"AS-{name.split('-')[1]}"

    # Parse 'Sala Informática Px', 'Aula de Informática Bx' , 'Aula Informática Sx' and 'Aula Bx' from Aulario Norte.
    result = re.search(r'02.01.01.00.((P1.00.0[3-6])|(P0.00.01.((1[2-7])|(0[189])))|(S1.00.(0[45789]|1[023])))', code)
    if bool(result):
        return f"AN-{name.split(' ')[-1].upper()}"

    # Parse 'Aula A' through 'Aula E' from Aulario Norte.
    result = re.search(r'02.01.01.00.P1.00.((0[7-9])|(1[0-1]))', code)
    if bool(result):
        return f"AN-{name.split(' ')[-1].upper()}"

    # Parse rooms with standard room codes (x.x.xx)
    result = re.search(r'\d\...?\.\d\d', name)
    if bool(result):
        return f"{EPI_BUILDING_CODES[building]}-{result.group(0).upper()}"

    # Parse 'Aula DO-1' through 'Aula DO -17'
    # No code-specific parsing is needed, names are unique and easily identifiable.
    # Same goes for Departamental Este below.
    result = re.search(r'^AULA DO ?-1?\d[A-B]?$', name.upper())
    if bool(result):
        do_final = result.group(0).replace('AULA ', '').replace(' ', '')
        if do_final.endswith('10'):  # DO-10 can be DO-10A or DO-10B.
            return f"{do_final}{name[-1]}"
        return do_final

    # Parse 'Aula DE-1' through 'Aula DE-8'.
    result = re.search(r'^AULA DE-[1-8]$', name.upper())
    if bool(result):
        return f"{result.group(0).replace('AULA ', '')}"

    # Parse Aula A2 through A6 and Aula A1 through A8 from Edificio Polivalente.
    result = re.search(r'02.01.08.00.P((1.00.06.0[1-5])|(0.00.0[2-9]))', code)
    if bool(result):
        return f"EP-{name.split(' ')[-1].upper()}"

    # If no match is found, return the original name including building and floor.
    return f"{EPI_BUILDING_CODES[building]}-{name} ({floor})"


# Parse the correct class name for each entry.
def parse_location(name, code) -> str:
    """
    método principal que se encarga de parsear el nombre de las aulas.

    Arguments:
        name {str} -- nombre del aula tal y como viene en el .ics
        code {str|None} -- código del aula tal obtenido de gis.uniovi.es
            Si no se proporciona, se devuelve el nombre sin parsear.
    """
    if code is None: return name  # if no code is provided, return name as is.


    try: building = code.split('.')[2]  # current building code
    except IndexError:  # should never happen, but this way it's more robust.
        return name

    # if location isn't in "Milla del Conocimiento Gijón" or building is outside of EPI Gijón, return location as is.
    if len(code.split('.')) < 5: return name
    floor = code.split('.')[4]
    if code.startswith(EPI_CODE) and building in EPI_BUILDING_CODES:
        return _parse_epi_location(name, code, building, floor)

    if code.startswith(EPM_CODE):
        # parseos específicos para Mieres
        return name.replace('Aula -', 'Aula')

    return name # if it wasn't parsed, return as it was.


# Parse the correct "class type" for each entry.
# Also parses the group for each entry except for "Clase Expositiva".
# AFAIK there are only "Teoría (CEX)", "Prácticas de Aula (PAx)", "Prácticas de Laboratorio (PLx)" and "Teorías Grupales (TGx)".
def parse_class_type(type) -> list[type[str]]:
    type_lower = type.lower().replace('.', '')  # lowercase and remove dots so it's easier to parse.
    class_group = type.replace('-', ' ').rsplit()[-1].strip('0').upper()

    # detect bilingual classes and replace with GB flag emoji.
    if class_group == "INGLÉS": class_group = "🇬🇧"
    lang = "🇬🇧" if "inglés" in type_lower or "ingles" in type_lower else ""

    # parse class type. it has to be as generic as possible because different subjects use different
    # abbreviations or styles for the same thing.
    if "teo" in type_lower or type_lower == "te" or "expositiv" in type_lower: return ['CEX', lang]
    if "tut" in type_lower or "grupal" in type_lower or type_lower == "tg": return ['TG', class_group]
    if "lab" in type_lower or type_lower == "pl": return ['PL', class_group]
    if "aula" in type_lower or type_lower == "pa": return ['PA', class_group]

    return [type, '']  # If the class type is not recognized, return the original string.
