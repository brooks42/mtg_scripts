# mtg_scripts

Scripts I threw together for various MTG-related products. Yes I'm a nerd.

### Cube compiler script

It's a collection of python scripts to build cube files from a given cockatrice XML file. Generates cube files for https://dr4ft.info/.

Run it like:

```
python3 [cube_compiler_script_name].py -f 'cards.xml'
```

#### Prereq's

You'll need to install BeautifulSoup using `pip`:

```
pip install beautifulsoup4
```

### Cockatrice

Get the XML file by installing https://github.com/Cockatrice/, and copying it over from there.

### Script descriptions

-   `all_cards_complier_script.py`: Generates a cube file with every card ever printed, minus subsets that don't _really_ make sense in draft, such as plane cards.
