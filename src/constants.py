entity_unit_map = {
    'width': {'cm', 'centimetre', 'centimeter', 'foot', 'ft', 'inch', '"', 'in', 'm', 'metre', 'meter', 'mm', 'millimetre', 'millimeter', 'yd', 'yard'},
    'depth': {'cm', 'centimetre', 'centimeter', 'foot', 'ft', 'inch', '"', 'in', 'm', 'metre', 'meter', 'mm', 'millimetre', 'millimeter', 'yd', 'yard'},
    'height': {'cm', 'centimetre', 'centimeter', 'foot', 'ft', 'inch', '"', 'in', 'm', 'metre', 'meter', 'mm', 'millimetre', 'millimeter', 'yd', 'yard'},
    'item_weight': {
        'g', 'gram', 'grams',
        'kg', 'kilogram', 'kilograms',
        'µg', 'mcg', 'microgram', 'micrograms',
        'mg', 'milligram', 'milligrams',
        'oz', 'ounce', 'ounces',
        'lb', 'lbs', 'pound', 'pounds',
        't', 'ton', 'tons'
    },
    'maximum_weight_recommendation': {
        'g', 'gram', 'grams',
        'kg', 'kilogram', 'kilograms',
        'µg', 'mcg', 'microgram', 'micrograms',
        'mg', 'milligram', 'milligrams',
        'oz', 'ounce', 'ounces',
        'lb', 'lbs', 'pound', 'pounds',
        't', 'ton', 'tons'
    },
    'voltage': {'kv', 'kilovolt', 'kilovolts', 'mv', 'millivolt', 'millivolts', 'v', 'volt', 'volts'},
    'wattage': {'kw', 'kilowatt', 'kilowatts', 'w', 'watt', 'watts'},
    'item_volume': {
        'cl', 'centilitre', 'centiliter',
        'cu ft', 'cubic foot', 'cubic feet',
        'cu in', 'cubic inch', 'cubic inches',
        'cup', 'cups',
        'dl', 'decilitre', 'deciliter',
        'fl oz', 'fluid ounce', 'fluid ounces',
        'gal', 'gallon', 'gallons',
        'imp gal', 'imperial gallon', 'imperial gallons',
        'l', 'liter', 'litre', 'liters', 'litres',
        'µl', 'microliter', 'microlitre', 'microliters', 'microlitres',
        'ml', 'milliliter', 'millilitre', 'milliliters', 'millilitres',
        'pt', 'pint', 'pints',
        'qt', 'quart', 'quarts'
    }
}

# Create a set of all allowed units
allowed_units = {unit.lower() for entity in entity_unit_map for unit in entity_unit_map[entity]}

# Create a dictionary to map various unit representations to their standard form
unit_standardization = {
    'cm': 'centimetre', 'centimeter': 'centimetre',
    'ft': 'foot', '"': 'inch', 'in': 'inch',
    'm': 'metre', 'meter': 'metre',
    'mm': 'millimetre', 'millimeter': 'millimetre',
    'yd': 'yard',
    'g': 'gram', 'grams': 'gram',
    'kg': 'kilogram', 'kilograms': 'kilogram',
    'µg': 'microgram', 'mcg': 'microgram', 'micrograms': 'microgram',
    'mg': 'milligram', 'milligrams': 'milligram',
    'oz': 'ounce', 'ounces': 'ounce',
    'lb': 'pound', 'lbs': 'pound', 'pounds': 'pound',
    't': 'ton', 'tons': 'ton',
    'kv': 'kilovolt', 'kilovolts': 'kilovolt',
    'mv': 'millivolt', 'millivolts': 'millivolt',
    'v': 'volt', 'volts': 'volt',
    'kw': 'kilowatt', 'kilowatts': 'kilowatt',
    'w': 'watt', 'watts': 'watt',
    'cl': 'centilitre', 'centiliter': 'centilitre',
    'cu ft': 'cubic foot', 'cubic feet': 'cubic foot',
    'cu in': 'cubic inch', 'cubic inches': 'cubic inch',
    'cups': 'cup',
    'dl': 'decilitre', 'deciliter': 'decilitre',
    'fl oz': 'fluid ounce', 'fluid ounces': 'fluid ounce',
    'gal': 'gallon', 'gallons': 'gallon',
    'imp gal': 'imperial gallon', 'imperial gallons': 'imperial gallon',
    'l': 'litre', 'liter': 'litre', 'liters': 'litre', 'litres': 'litre',
    'µl': 'microlitre', 'microliter': 'microlitre', 'microliters': 'microlitre', 'microlitres': 'microlitre',
    'ml': 'millilitre', 'milliliter': 'millilitre', 'milliliters': 'millilitre', 'millilitres': 'millilitre',
    'pt': 'pint', 'pints': 'pint',
    'qt': 'quart', 'quarts': 'quart'
}