# POGO AI

Please see `writing/project.pdf` for the final version of the paper.

The final project for the AI/ML course (CS 4100) at Northeastern.

Given a set of six defending Pokemon, determine the optimal set of six attacking Pokemon.

Greedy Best First Search and Monte Carlo Tree Search were implemented to solve this problem.

#### JSON Structures
- **Pokemon**
    ```json
    {
            "dex": 1, 
            "stats": {
                "base_stamina": 128, 
                "base_defense": 111, 
                "base_attack": 118
            }, 
            "name": "Bulbasaur", 
            "charge_moves": [
                "SLUDGE_BOMB", 
                "SEED_BOMB", 
                "POWER_WHIP"
            ], 
            "quick_moves": [
                "VINE_WHIP_FAST", 
                "TACKLE_FAST"
            ], 
            "types": [
                "POKEMON_TYPE_GRASS", 
                "POKEMON_TYPE_POISON"
            ]
        }
    ```
- **Type**
    ```json
    {
        "id": "POKEMON_TYPE_GRASS", 
        "damage": [
            {
                "id": "POKEMON_TYPE_NORMAL", 
                "multiplier": 1
            }, 
            {
                "id": "POKEMON_TYPE_FIGHTING", 
                "multiplier": 1
            }, 
            {
                "id": "POKEMON_TYPE_FLYING", 
                "multiplier": 0.714
            }, 
            ...
        ]
    }
    ```
- **Move**
    ```json
    {
        "power": 90, 
        "stamina_loss": 0.12, 
        "duration_ms": 2600, 
        "critical_chance": null, 
        "energy_delta": -50, 
        "type": "POKEMON_TYPE_GRASS", 
        "id": "POWER_WHIP", 
        "accuracy": 1
    }
    ```
    
- **data/**: Pokemon Go data
    - **old_raw/***: pokemon, move, and type data from [here](https://github.com/pokemongo-dev-contrib/pokemongo-json-pokedex)
    - **\*.json**: only information relevant for our project
- **utils/**: Utility functionality
    - **extract_data/**: Scripts to transform Pokemon data
    - **data_from_json.py**: Helper functions to get Python data from .json files
    - **json_utils.py**: Helper functions to help with dealing with JSON



