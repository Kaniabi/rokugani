# rokugani.model

The rokugani.model groups all the tools to create a Legend of Five Rings 4th character. This module
is completly interface independent.

This package is composed by four concepts:

## character-model

ChararacterModel holds all the information about a character including the numeric values and
modifiers.

The ChararacterModel holds many model-attributes in a dictionary (model). These attributes are called
model-attribute, and are all derived from the \_ModelAttrib class. Each different type of attribute
has its own class to implement any necessary details. The modifiers holds a list of modification
for model-attributes.

For example, the 'trait.intelligence' model-attribute holds the value 2 by default. Any changes in 
this value is done by adding modifiers. Each modifier not only hold information about the
model-attribute they are changing but also the source of the change (a rank, buy, skill, etc).

The function "explain_value" returns a list of all modifications for a model-attribute.

## data-access

The DataAccess class provides access to the rules database that are implemented in third party
projects (l5rcm-data-packs and l5rcm-data-access).

## character-builder

The CharacterBuilder provides the character creation logic, implementing all the character creation
rules. This class connects the character-model and data-access to implement the heart of the
application.

## advancements

Advancements are auxiliary classes for the character-builder. They serve to encapsulate the
advancement in objects so we can create, edit and delete them individually.
