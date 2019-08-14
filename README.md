# myShoppingList
## Snips - Assistant de cuisine 

Ce projet est mon premier projet d'assistant vocal Snips. Il  permet de gérer une liste de courses.

Pour la phase de tests, il est installé sur macOS, ensuite il sera déployé sur un  raspberry Pi.

>***Cet assistant sera complété par une app de gestion de mon blog de cuisine***

## Configuration

### MQTT

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `mqtt_host` | MQTT host name | `<ip address>`/`<hostname>` | `localhost` |
| `mqtt_port` | MQTT port number | `<mqtt port>` | `1883` |


### Mail Info

| Config | Description | Vaeur | Default |
| --- | --- | --- | --- |
| `default_user` | Snips User name | `<name>`  | `alain` |
| `mail_default_user` | mail of the user | <mail@address>  |  |
| `smtp_server` | SMTP server host name | `<smtp.domain>`  |  |
| `smtp_port` | SMTP port number | `<port>`  |25  |


### Media 

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `default_media` | Media used to send shopping list |  `<media name>` | `mail` |

### Printer 

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `default_printer` | Printer used to print shopping list |  `<printer name>` | `` |


