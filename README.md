# Nightscout (mmol/L) Integration for Home Assistant & Yandex Alice

**Connect your Nightscout glucose data to Home Assistant and Yandex Alice for advanced monitoring and voice control.**


## 🌟 Key Features
- **Home Assistant Integration**  
  📊 Real-time glucose data visualization  
  ⚡ Custom automations and alerts  
  📱 Mobile dashboard support

- **Yandex Alice Voice Control**  
  🎙️ Voice queries through Yandex Station  
  🔔 Spoken glucose alerts  
  💬 Natural language processing (*"Alice, what's my sugar?"*)

## 🛠 Installation & Setup

### 1. Prerequisites
- Working [Nightscout](https://nightscout.github.io/) setup
- [Home Assistant](https://www.home-assistant.io/) (v2023.12 or newer)
- Yandex Station with [Alice integration](https://yandex.ru/dev/dialogs/alice/)
- `tts.yandex_station_say` service enabled

### 2. Automation Configuration
Add to your `automations.yaml`:

```yaml
alias: "Оповещение Алисы о уровне глюкозы"
description: "Читает текущий уровень глюкозы вслух на колонке Яндекс"
mode: single

trigger:
  - platform: state
    entity_id: sensor.blood_sugar  # ← Replace with your sensor

action:
  - service: tts.yandex_station_say
    data:
      entity_id: "{{ station }}"
      message: >-
        {% set glucose = states('sensor.blood_sugar') %}
        {% set direction = state_attr('sensor.blood_sugar', 'direction') %}
        {% set delta = state_attr('sensor.blood_sugar', 'delta')|float(0) %}
        
        {# Trend translations #}
        {% set map = {
          'Flat': '→ стабильно',
          'SingleDown': '↓↓ быстро падает',
          'FortyFiveDown': '↘ снижается',
          'DoubleDown': '↓↓↓ резкое падение',
          'SingleUp': '↑↑ быстро растёт',
          'FortyFiveUp': '↗ повышается',
          'DoubleUp': '↑↑↑ резкий рост'
        } %}
        {% set trend = map.get(direction, '? неопределённый тренд') %}
        
        Глюкоза: {{ glucose }} ммоль/л. {{ trend }}.
        {% if delta > 0 %}
          Рост на {{ '%.1f'|format(delta) }} ммоль.
        {% elif delta < 0 %}
          Падение на {{ '%.1f'|format(delta|abs) }} ммоль.
        {% endif %}

variables:
  station: media_player.yandex_station_your_device_id  # ← Update this
```


# Yandex Station Glucose Monitoring Integration

## 3. Customization Guide

| Setting             | Description                     | Example                          |
|---------------------|---------------------------------|----------------------------------|
| `sensor.blood_sugar` | Your glucose sensor entity      | `sensor.nightscout_glucose`      |
| `station variable`  | Yandex Station device ID        | `media_player.yandex_station_123abc` |
| `Message template`  | Customize spoken phrases        | `"Внимание! {{ glucose }} ммоль"` |

💡 **Usage Examples**

### Voice Commands:
- "Алиса, какой у меня сахар?"
- "Алиса, скажи тренд глюкозы"

### Home Assistant Automations:
```yaml
- alias: "Hypo Alert"
  trigger:
    platform: numeric_state
    entity_id: sensor.blood_sugar
    below: 4.0
  action:
    - service: tts.yandex_station_say
      data:
        message: "Внимание! Низкий сахар: {{ states('sensor.blood_sugar') }} ммоль!"
```