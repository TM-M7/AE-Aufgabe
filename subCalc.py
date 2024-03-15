import dearpygui.dearpygui as dpg
import math

dpg.create_context()

# Definieren Farben für die Benutzeroberfläche
hintergrundfarbe = [25, 25, 25]  # grau
textfarbe = [255, 255, 255]  # weiß
akzentfarbe = [255, 87, 51]  # orange
sekundaere_farbe = [150, 0, 255]  # violett

# Benutzerdefinierte Themen für Widgets verwenden
with dpg.theme() as button_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, akzentfarbe)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 140, 90])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [255, 100, 70])
        dpg.add_theme_color(dpg.mvThemeCol_Text, textfarbe)

class SubnetCalculator:
    @staticmethod
    def subnetze_berechnen(basis_netz, anzahl_subnetze):
        oktetten = list(map(int, basis_netz.split('.')))
        if len(oktetten) != 4 or oktetten[3] != 0:
            raise ValueError("Das Basisnetz muss im Format xxx.xxx.xxx.0 sein.")

        benoetigte_bits = math.ceil(math.log2(anzahl_subnetze))
        if benoetigte_bits > 8:
            raise ValueError("Zu viele Subnetze für ein /24 Netz.")

        neue_subnetz_maske = 24 + benoetigte_bits
        host_bits = 32 - neue_subnetz_maske
        max_hosts = (2 ** host_bits) - 2

        if max_hosts < 2:
            raise ValueError("Zu viele Subnetze, nicht genug Hosts pro Subnetz.")

        inkrement = 2 ** (8 - benoetigte_bits)
        subnetze = []
        for i in range(anzahl_subnetze):
            oktetten[3] = i * inkrement
            subnetze.append('.'.join(map(str, oktetten)))

        return neue_subnetz_maske, max_hosts, subnetze

def berechnen_callback(sender, app_data, user_data):
    basis_netz = dpg.get_value("basis_netz_input")
    anzahl_subnetze = dpg.get_value("anzahl_subnetze_input")
    
    # Überprüfen Sie, ob die Eingabefelder leer sind, bevor Sie fortfahren
    if not basis_netz or not anzahl_subnetze or not anzahl_subnetze.isdigit():
        dpg.set_value("ergebnis_output", "Bitte geben Sie gültige Werte ein.")
        return
    
    try:
        neue_subnetz_maske, max_hosts, subnetze = SubnetCalculator.subnetze_berechnen(basis_netz, int(anzahl_subnetze))
        ergebnis_text = f"Neue Subnetzmaske: /{neue_subnetz_maske} mit max. {max_hosts} Hosts pro Subnetz.\n"
        ergebnis_text += "\n".join(f"Subnetz {i+1}: {subnet}" for i, subnet in enumerate(subnetze))
        dpg.set_value("ergebnis_output", ergebnis_text)  # Ergebnisse anzeigen
    except ValueError as e:
        dpg.set_value("ergebnis_output", str(e))  # Fehlermeldung anzeigen

with dpg.window(label="Subnetzrechner", width=600, height=300):
    dpg.add_text("Basisnetz (z. B. 192.168.1.0):", color=textfarbe)
    basis_netz_input = dpg.add_input_text(tag="basis_netz_input")
    dpg.add_text("Anzahl der Subnetze:", color=textfarbe)
    anzahl_subnetze_input = dpg.add_input_text(tag="anzahl_subnetze_input")
    
    dpg.add_button(label="Berechnen", callback=berechnen_callback, tag="berechnen_button")
    dpg.bind_item_theme("berechnen_button", button_theme)  #Anwendung des Thema auf die Schaltfläche an
    dpg.add_text("", tag="ergebnis_output", color=sekundaere_farbe)

# Viewport mit angepassten Farben erstellen
dpg.create_viewport(title='Subnetzrechner Heinrich Doroshenko', width=600, height=300)
dpg.set_viewport_clear_color(hintergrundfarbe)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()