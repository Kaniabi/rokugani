# Rokugani
L5R Character Editor

## Introduction

This is a playground to test some ideas regarding modeling a RPG character editor.

## Design

The CharacterModel has a dictionary with objects (called model-attributes). Each (many) of these objects have a value property interface that can be accessed directly or using the model "get_value" function.

The get_value function is key here because it not only returns the model-attribute value but also adds/subtracts bonuses defined on the modifiers.

The explain_value returns a list of modifiers applied to that model-attribute value.

