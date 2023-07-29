prompt = """Your task is to match address entities given in the list \"client_entities\" (enclosed within <<<>>>) with entities present in the list \"database_entities\" (also enclosed within <<<>>>). Each entity within the lists \"database_entities\" and \"client_entities\" is enclosed within double quotes. 

You must make sure to not map two entities when the difference between the area/region covered by the two entities is very high. For example, you must not map \"state\" to \"landmark\" as the region covered by \"landmark\" is very small when compared to \"state\".

For each value within the \"client_entities\" list, try to find the most suitable value from the \"database_entities\" list. Your output must be in json format where each key is an entity from the list \"client_entities\" and the corresponding value is the most similar entity from the list \"database_entities\". If you are not able to find any meaningful match for a value in \"client_entities\" within \"database_entities\" list, then you must not generate any output corresponding to that value in the json output.

input: <<<client_entities: [\"Name\", \"10-digit Mobile Number\", \"pincode\", \"locality\", \"Address (area and street)\", \"City/District/Town\", \"State\", \"Landmark (optional)\", \"Alternate Phone (optional)\"]>>>

<<<database_entities: [\"name\", \"phone no\", \"pin\", \"flat\", \"city\", \"landmark\"]>>>
output: {
  \"Name\": \"name\",
  \"10-digit Mobile Number\": \"phone no\",
  \"pincode\": \"pin\",
  \"locality\": \"flat\",
  \"Address (area and street)\": \"flat\",
  \"City/District/Town\": \"city\",
  \"Landmark (optional)\": \"landmark\",
}

input: <<<client_entities: [\"Name\", \"10-digit Mobile Number\", \"H.No\", \"pin\", \"locality\", \"Address (area and street)\", \"City/District/Town\", \"State\", \"Landmark (optional)\", \"Alternate Phone (optional)\"]>>>

<<<database_entities: [\"name\", \"phone no\", \"pincode\", \"house\", \"city\", \"landmark\", \"state\", \"society\", \"town\", \"district\"]>>>
output: {
  \"Name\": \"name\",
  \"10-digit Mobile Number\": \"phone no\",
  \"H.No\": \"house\",
  \"pin\": \"pin code\",
  \"locality\": \"district\",
  \"City/District/Town\": \"city\",
  \"State\": \"state\",
  \"Landmark (optional)\": \"landmark\",
}


input: <<<client_entities: [\"Full Name\", \"Mobile Number\", \"Pincode\", \"Flat, House no., Building, Company, \"Apartment\", \"Area, Street, Sector, Village\", \"Landmark\", \"Town/City\", \"State\"]>>>

<<<database_entities: [\"name\", \"phone no\", \"pin_code\", \"house\", \"city\", \"landmark\", \"state\", \"society\", \"town\"]>>>
output: {
  \"Full Name\": \"name\",
  \"Mobile Number\": \"phone no\",
  \"Pincode\": \"pin_code\",
  \"Flat, House no., Building, Company, \"Apartment\": \"house\",
  \"Area, Street, Sector, Village\": \"society\",
  \"Landmark\": \"landmark\",
  \"Town/City\": \"town\",
  \"State\": \"state\",
}


input: <<<client_entities: [\"Name\", \"Mobile\", \"Pincode\", \"State\", \"Address (House no., Building, Street, Area)\",  \"Locality/Town\",  \"City/District\"]>>>

<<<database_entities: [\"name\", \"phone no\", \"pin_code\", \"house\", \"city\", \"landmark\", \"state\", \"society\", \"town\"]>>>
output: {
  \"Name\": \"name\",
  \"Mobile\": \"phone no\",
  \"Pincode\": \"pin_code\",
  \"State\": \"state\",
  \"Address (House no., Building, Street, Area)\": \"house\",
  \"Locality/Town\": \"town\",
  \"City/District\": \"city\",
}


input: <<<client_entities: [\"Name\", \"Mobile\", \"Pincode\", \"State\", \"Address (House no., Building, Street, Area)\",  \"Locality/Town\",  \"City/District\"]>>>

<<<database_entities: [\"name\", \"phone no\"]>>>
output: {
  \"Name\": \"name\",
  \"Mobile\": \"phone no\",
}


input: <<<client_entities: [\"Name\", \"Flat\", \"pin\"]>>>

<<<database_entities: [\"name\", \"phone no\", \"pin_code\", \"house\", \"city\", \"landmark\", \"state\", \"society\", \"town\"]>>>
output: {
  \"Name\": \"name\",
  \"Flat\": \"house\",
  \"pin\": \"pin_code\",
}


input: <<<client_entities: [\"full name\", \"10 digit mobile number\", \"area\"]>>>

<<<database_entities: []>>>
output: {}


input: <<<client_entities: [\'pincode\', \'state\', \'locality\', \'landmark\', \'city\']>>>

<<<database_entities: [\"village\", \"city\", \"state\", \"pincode\", \"landmark\", \"door\",\"country\"]>>>
output: {
  \"pincode\": \"pincode\",
  \"state\": \"state\",
  \"locality\": \"village\",
  \"landmark\": \"landmark\",
  \"city\": \"city\",
}


input: <<<client_entities: [\"name\", \"pincode\", \"flat\", \"area\", \"locality\", \"state\"]>>>

<<<database_entities: [\"house number\", \"village\"]>>>
output: {
  \"house number\": \"flat\",
  \"locality\": \"village\"
}
"""