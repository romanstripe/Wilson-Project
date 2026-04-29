#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"

static void csi_cb(void *ctx, wifi_csi_info_t *data)
{
    Serial.print("CSI len: ");
    Serial.println(data->len);

    for(int i=0;i<data->len;i++){
        Serial.print(data->buf[i]);
        Serial.print(",");
    }

    Serial.println();
}

void setup() {

Serial.begin(115200);

nvs_flash_init();
esp_event_loop_create_default();

wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
esp_wifi_init(&cfg);

esp_wifi_set_mode(WIFI_MODE_STA);
esp_wifi_start();

wifi_config_t sta_config = {};
strcpy((char*)sta_config.sta.ssid, "GRADUATION_PROJECT");
strcpy((char*)sta_config.sta.password, "12345678");

esp_wifi_set_config(WIFI_IF_STA, &sta_config);
esp_wifi_connect();

Serial.println("Connecting to AP...");

esp_wifi_set_channel(11, WIFI_SECOND_CHAN_NONE);

wifi_csi_config_t config;

config.lltf_en = 1;
config.htltf_en = 1;
config.stbc_htltf2_en = 1;
config.ltf_merge_en = 1;
config.channel_filter_en = 0;
config.manu_scale = 0;
config.shift = 0;

esp_wifi_set_promiscuous(true);

esp_wifi_set_csi_rx_cb(csi_cb, NULL);
esp_wifi_set_csi_config(&config);
esp_wifi_set_csi(true);

Serial.println("CSI STARTED");

}

void loop() {}
