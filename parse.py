import re

buildingCodes = {  # building codes for 'Milla del Conocimiento' (Gijón 02.01) sourced from gis.uniovi.es
    '01': 'AN',
    '02': 'AS',
    '04': 'DE',
    '05': 'DO',
    '08': 'EP'
}


# Parse the correct class name for each entry.
def parseLocation(loc, codEspacio):
    try: buildingCode = codEspacio.split('.')[2]  # current building code
    except IndexError:  # should never happen, but this way it's more robust.
        return loc

    # if location isn't in "Milla del Conocimiento Gijón" or building is outside of EPI Gijón, return location as is.
    floor = codEspacio.split('.')[4]
    if not codEspacio[:5] == "02.01" or buildingCode not in buildingCodes: return loc

    # Aula AS-1 through Aula AS-11
    result = re.search(r'02.01.02.00.P1.00.(0[1-9]|1[0-1])', codEspacio)
    if bool(result):
        return f"AS-{loc.split('-')[1]}"

    # Parse 'Sala Informática Px', 'Aula de Informática Bx' , 'Aula Informática Sx' and 'Aula Bx' from Aulario Norte.
    result = re.search(r'02.01.01.00.((P1.00.0[3-6])|(P0.00.01.((1[2-7])|(0[189])))|(S1.00.(0[45789]|1[023])))', codEspacio)
    if bool(result):
        return f"AN-{loc.split(' ')[-1].upper()}"

    # Parse 'Aula A' through 'Aula E' from Aulario Norte.
    result = re.search(r'02.01.01.00.P1.00.((0[7-9])|(1[0-1]))', codEspacio)
    if bool(result):
        return f"AN-{loc.split(' ')[-1].upper()}"

    # Parse rooms with standard room codes (x.x.xx)
    result = re.search(r'\d\...?\.\d\d', loc)
    if bool(result):
        return f"{buildingCodes[buildingCode]}-{result.group(0).upper()}"

    # Parse 'Aula DO-1' through 'Aula DO -17'
    # No code-specific parsing is needed, names are unique and easily identifiable.
    # Same goes for Departamental Este below.
    result = re.search(r'^AULA DO[ ]?-1?\d[A-B]?$', loc.upper())
    if bool(result):
        doFinal = result.group(0).replace('AULA ', '').replace(' ', '')
        if doFinal[-2:] == "10":  # DO-10 can be DO-10A or DO-10B.
            return f"{doFinal}{loc[-1]}"
        return doFinal

    # Parse 'Aula DE-1' through 'Aula DE-8'.
    result = re.search(r'^AULA DE-[1-8]$', loc.upper())
    if bool(result):
        return f"{result.group(0).replace('AULA ', '')}"

    # Parse Aula A2 through A6 and Aula A1 through A8 from Edificio Polivalente.
    result = re.search(r'02.01.08.00.P((1.00.06.0[1-5])|(0.00.0[2-9]))', codEspacio)
    if bool(result):
        return f"EP-{loc.split(' ')[-1].upper()}"

    # If no match is found, return the original name including building and floor.
    return f"{buildingCodes[buildingCode]}-{loc} ({floor})"


# Parse the correct "class type" for each entry.
# Also parses the group for each entry except for "Clase Expositiva".
# AFAIK there are only "Teoría (CEX)", "Prácticas de Aula (PAx)", "Prácticas de Laboratorio (PLx)" and "Teorías Grupales (TGx)".
def parseClassType(type):
    typeL = type.lower().replace('.', '')  # lowercase and remove dots so it's easier to parse.
    classGroup = type.replace('-', ' ').rsplit()[-1].strip('0').upper()

    # detect bilingual classes and replace with GB flag emoji.
    if classGroup == "INGLÉS": classGroup = "🇬🇧"
    lang = "🇬🇧" if "inglés" in typeL or "ingles" in typeL else ""

    # parse class type. it has to be as generic as possible because different subjects use different
    # abbreviations or styles for the same thing.
    if "teo" in typeL or typeL == "te" or "expositiv" in typeL: return f"CEX{lang}"
    if "tut" in typeL or "grupal" in typeL or typeL == "tg": return f"TG{classGroup}"
    if "lab" in typeL or typeL == "pl": return f"PL{classGroup}"
    if "aula" in typeL or typeL == "pa": return f"PA{classGroup}"

    return type  # If the class type is not recognized, return the original string.
