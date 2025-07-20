import { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  ScrollView,
  Switch,
  Alert,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
  Modal,
} from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";

const API_URL = "http://localhost:8000/config";

type DownloadClientConfig = {
  tags: string[];
  client_type: string;
  client_ip: string;
  client_username: string;
  client_password: string;
  client_port: number;
};

type Config = {
  database: {
    host: string;
    port: number;
    database: string;
    user: string;
    password: string;
    echo: boolean;
    pool_size: number;
    max_overflow: number;
  };
  api: {
    title: string;
    version: string;
    description: string;
    debug: boolean;
    cors_origins: string[];
    host: string;
    port: number;
  };
  external_apis: {
    hardcover_api_key: string;
    inventaire_enabled: boolean;
    rate_limit_requests: number;
    rate_limit_window: number;
    timeout: number;
  };
  logging: {
    level: string;
    format: string;
    rotation: string;
    retention: string;
    file_path: string | null;
  };
  security: {
    secret_key: string;
    algorithm: string;
    access_token_expire_minutes: number;
  };
  download_clients: DownloadClientConfig[];
  // Add other config sections as needed
};

export default function ConfigPage() {
  const [config, setConfig] = useState<Config | null>(null);
  const [originalConfig, setOriginalConfig] = useState<Config | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [health, setHealth] = useState<ConfigHealth | null>(null);
  const [showRawEditor, setShowRawEditor] = useState(false);
  const [rawToml, setRawToml] = useState("");
  const [hasChanges, setHasChanges] = useState(false);
  const [downloadClientTypes, setDownloadClientTypes] = useState<string[]>([]);

  useEffect(() => {
    loadConfig();
    loadHealth();
    fetchDownloadClientTypes();
  }, []);

  useEffect(() => {
    if (config && originalConfig) {
      setHasChanges(JSON.stringify(config) !== JSON.stringify(originalConfig));
    }
  }, [config, originalConfig]);

  const loadConfig = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Failed to load config");
      const data = await response.json();
      setConfig(data);
      setOriginalConfig(JSON.parse(JSON.stringify(data)));
    } catch (error) {
      Alert.alert("Error", "Failed to load configuration");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      if (!response.ok) throw new Error("Failed to load health");
      const data = await response.json();
      setHealth(data);
    } catch (error) {
      console.error("Failed to load health:", error);
    }
  };

  const loadRawConfig = async () => {
    try {
      const response = await fetch(`${API_URL}/raw`);
      if (!response.ok) throw new Error("Failed to load raw config");
      const data = await response.json();
      setRawToml(data.toml);
    } catch (error) {
      Alert.alert("Error", "Failed to load raw configuration");
      console.error(error);
    }
  };

  const saveConfig = async () => {
    try {
      setSaving(true);
      const response = await fetch(API_URL, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to save config");
      }

      setOriginalConfig(JSON.parse(JSON.stringify(config)));
      Alert.alert("Success", "Configuration saved successfully");
      await loadHealth(); // Refresh health status
    } catch (error) {
      Alert.alert("Error", `Failed to save configuration: ${error.message}`);
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  const saveRawConfig = async () => {
    try {
      setSaving(true);
      const response = await fetch(`${API_URL}/raw`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ toml_content: rawToml }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to save raw config");
      }

      Alert.alert("Success", "Raw configuration saved successfully");
      await loadConfig(); // Reload the structured config
      setShowRawEditor(false);
    } catch (error) {
      Alert.alert(
        "Error",
        `Failed to save raw configuration: ${error.message}`
      );
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  const reloadConfig = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/reload`, { method: "POST" });
      if (!response.ok) throw new Error("Failed to reload config");

      await loadConfig();
      await loadHealth();
      Alert.alert("Success", "Configuration reloaded from file");
    } catch (error) {
      Alert.alert("Error", "Failed to reload configuration");
      console.error(error);
    }
  };

  const resetChanges = () => {
    if (originalConfig) {
      setConfig(JSON.parse(JSON.stringify(originalConfig)));
    }
  };

  const updateConfigValue = (section: string, key: string, value: any) => {
    if (!config) return;

    setConfig((prev) => ({
      ...prev!,
      [section]: {
        ...prev![section],
        [key]: value,
      },
    }));
  };

  const addCorsOrigin = (newOrigin: string) => {
    if (!config || !newOrigin.trim()) return;

    const currentOrigins = config.api.cors_origins || [];
    if (!currentOrigins.includes(newOrigin.trim())) {
      updateConfigValue("api", "cors_origins", [
        ...currentOrigins,
        newOrigin.trim(),
      ]);
    }
  };

  const removeCorsOrigin = (origin: string) => {
    if (!config) return;

    const currentOrigins = config.api.cors_origins || [];
    updateConfigValue(
      "api",
      "cors_origins",
      currentOrigins.filter((o) => o !== origin)
    );
  };

  const addDownloadClient = () => {
    if (!config || downloadClientTypes.length === 0) return;
    const defaultType = downloadClientTypes[0];
    const newClient: DownloadClientConfig = {
      tags: [],
      client_type: defaultType,
      client_ip: "",
      client_username: "",
      client_password: "",
      client_port: 8080,
    };
    setConfig((prev) => ({
      ...prev!,
      download_clients: [...(prev!.download_clients || []), newClient],
    }));
  };

  const updateDownloadClient = (index: number, key: string, value: any) => {
    if (!config) return;
    const updatedClients = config.download_clients.map((client, i) =>
      i === index ? { ...client, [key]: value } : client
    );
    setConfig((prev) => ({
      ...prev!,
      download_clients: updatedClients,
    }));
  };

  const removeDownloadClient = (index: number) => {
    if (!config) return;
    const updatedClients = config.download_clients.filter(
      (_, i) => i !== index
    );
    setConfig((prev) => ({
      ...prev!,
      download_clients: updatedClients,
    }));
  };

  const fetchDownloadClientTypes = async () => {
    try {
      const response = await fetch(`${API_URL}/download-client-types`);
      if (!response.ok) throw new Error("Failed to fetch client types");
      const data = await response.json();
      setDownloadClientTypes(data.types || []);
    } catch (error) {
      setDownloadClientTypes([
        "qbittorrent",
        "aria2",
        "transmission",
        "deluge",
      ]); // fallback
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, configStyles.centered]}>
        <ActivityIndicator size="large" color="#0066cc" />
        <Text style={configStyles.loadingText}>Loading configuration...</Text>
      </View>
    );
  }

  if (!config) {
    return (
      <View style={[styles.container, configStyles.centered]}>
        <Text style={configStyles.errorText}>Failed to load configuration</Text>
        <Button title="Retry" onPress={loadConfig} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={configStyles.scrollContainer}>
        {/* Header with health status */}
        <View style={configStyles.header}>
          <Text style={configStyles.title}>Configuration</Text>
          {health && (
            <View
              style={[
                configStyles.healthBadge,
                health.status === "healthy"
                  ? configStyles.healthyBadge
                  : configStyles.unhealthyBadge,
              ]}
            >
              <Text style={configStyles.healthText}>
                {health.status.toUpperCase()} - {health.environment} v
                {health.version}
              </Text>
            </View>
          )}
        </View>

        {/* Action buttons */}
        <View style={configStyles.actionBar}>
          <TouchableOpacity
            style={[configStyles.button, configStyles.secondaryButton]}
            onPress={() => {
              loadRawConfig();
              setShowRawEditor(true);
            }}
          >
            <Text style={configStyles.buttonText}>Raw Editor</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[configStyles.button, configStyles.secondaryButton]}
            onPress={reloadConfig}
          >
            <Text style={configStyles.buttonText}>Reload</Text>
          </TouchableOpacity>

          {hasChanges && (
            <TouchableOpacity
              style={[configStyles.button, configStyles.warningButton]}
              onPress={resetChanges}
            >
              <Text style={configStyles.buttonText}>Reset</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Database Configuration */}
        <View style={configStyles.section}>
          <Text style={configStyles.sectionTitle}>Database</Text>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Host:</Text>
            <TextInput
              style={configStyles.input}
              value={config.database.host}
              onChangeText={(value) =>
                updateConfigValue("database", "host", value)
              }
              placeholder="localhost"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Port:</Text>
            <TextInput
              style={configStyles.input}
              value={config.database.port.toString()}
              onChangeText={(value) =>
                updateConfigValue("database", "port", parseInt(value) || 5432)
              }
              keyboardType="numeric"
              placeholder="5432"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Database:</Text>
            <TextInput
              style={configStyles.input}
              value={config.database.database}
              onChangeText={(value) =>
                updateConfigValue("database", "database", value)
              }
              placeholder="fastlibrarian"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>User:</Text>
            <TextInput
              style={configStyles.input}
              value={config.database.user}
              onChangeText={(value) =>
                updateConfigValue("database", "user", value)
              }
              placeholder="fastlib"
            />
          </View>

          <View style={configStyles.switchRow}>
            <Text style={configStyles.label}>Echo SQL:</Text>
            <Switch
              value={config.database.echo}
              onValueChange={(value) =>
                updateConfigValue("database", "echo", value)
              }
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Pool Size:</Text>
            <TextInput
              style={configStyles.input}
              value={config.database.pool_size.toString()}
              onChangeText={(value) =>
                updateConfigValue(
                  "database",
                  "pool_size",
                  parseInt(value) || 10
                )
              }
              keyboardType="numeric"
              placeholder="10"
            />
          </View>
        </View>

        {/* API Configuration */}
        <View style={configStyles.section}>
          <Text style={configStyles.sectionTitle}>API</Text>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Title:</Text>
            <TextInput
              style={configStyles.input}
              value={config.api.title}
              onChangeText={(value) => updateConfigValue("api", "title", value)}
              placeholder="FastLibrarian API"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Description:</Text>
            <TextInput
              style={[configStyles.input, configStyles.multilineInput]}
              value={config.api.description}
              onChangeText={(value) =>
                updateConfigValue("api", "description", value)
              }
              placeholder="API description"
              multiline
              numberOfLines={3}
            />
          </View>

          <View style={configStyles.switchRow}>
            <Text style={configStyles.label}>Debug Mode:</Text>
            <Switch
              value={config.api.debug}
              onValueChange={(value) =>
                updateConfigValue("api", "debug", value)
              }
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Port:</Text>
            <TextInput
              style={configStyles.input}
              value={config.api.port.toString()}
              onChangeText={(value) =>
                updateConfigValue("api", "port", parseInt(value) || 8000)
              }
              keyboardType="numeric"
              placeholder="8000"
            />
          </View>

          {/* CORS Origins */}
          <View style={configStyles.subsection}>
            <Text style={configStyles.subsectionTitle}>CORS Origins</Text>
            {config.api.cors_origins.map((origin, index) => (
              <View key={index} style={configStyles.corsRow}>
                <Text style={configStyles.corsOrigin}>{origin}</Text>
                <TouchableOpacity onPress={() => removeCorsOrigin(origin)}>
                  <Text style={configStyles.removeButton}>Remove</Text>
                </TouchableOpacity>
              </View>
            ))}
            <View style={configStyles.row}>
              <TextInput
                style={[configStyles.input, { flex: 1 }]}
                placeholder="Add new CORS origin"
                onSubmitEditing={(e) => {
                  addCorsOrigin(e.nativeEvent.text);
                  e.target.clear();
                }}
              />
            </View>
          </View>
        </View>

        {/* External APIs */}
        <View style={configStyles.section}>
          <Text style={configStyles.sectionTitle}>External APIs</Text>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Hardcover API Key:</Text>
            <TextInput
              style={configStyles.input}
              value={config.external_apis.hardcover_api_key}
              onChangeText={(value) =>
                updateConfigValue("external_apis", "hardcover_api_key", value)
              }
              placeholder="Enter API key"
              secureTextEntry
            />
          </View>

          <View style={configStyles.switchRow}>
            <Text style={configStyles.label}>Inventaire Enabled:</Text>
            <Switch
              value={config.external_apis.inventaire_enabled}
              onValueChange={(value) =>
                updateConfigValue("external_apis", "inventaire_enabled", value)
              }
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Rate Limit (requests):</Text>
            <TextInput
              style={configStyles.input}
              value={config.external_apis.rate_limit_requests.toString()}
              onChangeText={(value) =>
                updateConfigValue(
                  "external_apis",
                  "rate_limit_requests",
                  parseInt(value) || 100
                )
              }
              keyboardType="numeric"
              placeholder="100"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Timeout (seconds):</Text>
            <TextInput
              style={configStyles.input}
              value={config.external_apis.timeout.toString()}
              onChangeText={(value) =>
                updateConfigValue(
                  "external_apis",
                  "timeout",
                  parseFloat(value) || 30.0
                )
              }
              keyboardType="numeric"
              placeholder="30.0"
            />
          </View>
        </View>

        {/* Logging Configuration */}
        <View style={configStyles.section}>
          <Text style={configStyles.sectionTitle}>Logging</Text>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Level:</Text>
            <View style={configStyles.pickerContainer}>
              {["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"].map(
                (level) => (
                  <TouchableOpacity
                    key={level}
                    style={[
                      configStyles.pickerOption,
                      config.logging.level === level &&
                        configStyles.pickerOptionSelected,
                    ]}
                    onPress={() => updateConfigValue("logging", "level", level)}
                  >
                    <Text
                      style={[
                        configStyles.pickerOptionText,
                        config.logging.level === level &&
                          configStyles.pickerOptionTextSelected,
                      ]}
                    >
                      {level}
                    </Text>
                  </TouchableOpacity>
                )
              )}
            </View>
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Rotation:</Text>
            <TextInput
              style={configStyles.input}
              value={config.logging.rotation}
              onChangeText={(value) =>
                updateConfigValue("logging", "rotation", value)
              }
              placeholder="10 MB"
            />
          </View>

          <View style={configStyles.row}>
            <Text style={configStyles.label}>Retention:</Text>
            <TextInput
              style={configStyles.input}
              value={config.logging.retention}
              onChangeText={(value) =>
                updateConfigValue("logging", "retention", value)
              }
              placeholder="7 days"
            />
          </View>
        </View>

        {/* Download Clients Section */}
        <View style={configStyles.section}>
          <Text style={configStyles.sectionTitle}>Download Clients</Text>
          {config.download_clients && config.download_clients.length > 0 ? (
            config.download_clients.map((client, idx) => (
              <View
                key={idx}
                style={[configStyles.subsection, { marginBottom: 16 }]}
              >
                <Text style={configStyles.subsectionTitle}>
                  Client #{idx + 1}
                </Text>
                <View style={configStyles.row}>
                  <Text style={configStyles.label}>Type:</Text>
                  <View style={configStyles.pickerContainer}>
                    {downloadClientTypes.map((type) => (
                      <TouchableOpacity
                        key={type}
                        style={[
                          configStyles.pickerOption,
                          client.client_type === type &&
                            configStyles.pickerOptionSelected,
                        ]}
                        onPress={() =>
                          updateDownloadClient(idx, "client_type", type)
                        }
                      >
                        <Text
                          style={[
                            configStyles.pickerOptionText,
                            client.client_type === type &&
                              configStyles.pickerOptionTextSelected,
                          ]}
                        >
                          {type}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>
                <View style={configStyles.row}>
                  <Text style={configStyles.label}>IP:</Text>
                  <TextInput
                    style={configStyles.input}
                    value={client.client_ip}
                    onChangeText={(v) =>
                      updateDownloadClient(idx, "client_ip", v)
                    }
                    placeholder="Client IP Address"
                  />
                </View>
                <View style={configStyles.row}>
                  <Text style={configStyles.label}>Username:</Text>
                  <TextInput
                    style={configStyles.input}
                    value={client.client_username}
                    onChangeText={(v) =>
                      updateDownloadClient(idx, "client_username", v)
                    }
                    placeholder="Client username"
                  />
                </View>
                <View style={configStyles.row}>
                  <Text style={configStyles.label}>Password:</Text>
                  <TextInput
                    style={configStyles.input}
                    value={client.client_password}
                    onChangeText={(v) =>
                      updateDownloadClient(idx, "client_password", v)
                    }
                    placeholder="Client password"
                    secureTextEntry
                  />
                </View>
                <View style={configStyles.row}>
                  <Text style={configStyles.label}>Port:</Text>
                  <TextInput
                    style={configStyles.input}
                    value={client.client_port.toString()}
                    onChangeText={(v) =>
                      updateDownloadClient(
                        idx,
                        "client_port",
                        parseInt(v) || 8080
                      )
                    }
                    keyboardType="numeric"
                    placeholder="Client Port"
                  />
                </View>
                <TouchableOpacity
                  style={[
                    configStyles.button,
                    configStyles.warningButton,
                    { marginTop: 8 },
                  ]}
                  onPress={() => removeDownloadClient(idx)}
                >
                  <Text style={configStyles.buttonText}>Remove Client</Text>
                </TouchableOpacity>
              </View>
            ))
          ) : (
            <Text style={{ color: "#888" }}>
              No download clients configured.
            </Text>
          )}
          <TouchableOpacity
            style={[
              configStyles.button,
              configStyles.primaryButton,
              { marginTop: 8 },
              downloadClientTypes.length === 0 && configStyles.disabledButton,
            ]}
            onPress={addDownloadClient}
            disabled={downloadClientTypes.length === 0}
          >
            <Text style={configStyles.buttonText}>Add Download Client</Text>
          </TouchableOpacity>
        </View>

        {/* Save button */}
        <View style={configStyles.saveContainer}>
          <TouchableOpacity
            style={[
              configStyles.button,
              configStyles.primaryButton,
              (!hasChanges || saving) && configStyles.disabledButton,
            ]}
            onPress={saveConfig}
            disabled={!hasChanges || saving}
          >
            <Text style={configStyles.buttonText}>
              {saving
                ? "Saving..."
                : hasChanges
                ? "Save Changes"
                : "No Changes"}
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* Raw TOML Editor Modal */}
      <Modal
        visible={showRawEditor}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <View style={configStyles.modalContainer}>
          <View style={configStyles.modalHeader}>
            <Text style={configStyles.modalTitle}>Raw TOML Editor</Text>
            <TouchableOpacity onPress={() => setShowRawEditor(false)}>
              <Text style={configStyles.closeButton}>Close</Text>
            </TouchableOpacity>
          </View>

          <TextInput
            style={configStyles.rawEditor}
            value={rawToml}
            onChangeText={setRawToml}
            multiline
            placeholder="TOML configuration..."
            textAlignVertical="top"
          />

          <View style={configStyles.modalActions}>
            <TouchableOpacity
              style={[configStyles.button, configStyles.primaryButton]}
              onPress={saveRawConfig}
              disabled={saving}
            >
              <Text style={configStyles.buttonText}>
                {saving ? "Saving..." : "Save Raw Config"}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const configStyles = StyleSheet.create({
  scrollContainer: {
    flex: 1,
  },
  centered: {
    justifyContent: "center",
    alignItems: "center",
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: "#666",
  },
  errorText: {
    fontSize: 16,
    color: "#ff4444",
    marginBottom: 20,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#333",
  },
  healthBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  healthyBadge: {
    backgroundColor: "#4caf50",
  },
  unhealthyBadge: {
    backgroundColor: "#f44336",
  },
  healthText: {
    color: "white",
    fontSize: 12,
    fontWeight: "bold",
  },
  actionBar: {
    flexDirection: "row",
    padding: 16,
    gap: 8,
  },
  section: {
    backgroundColor: "white",
    margin: 8,
    padding: 16,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#333",
    marginBottom: 12,
  },
  subsection: {
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: "#e0e0e0",
  },
  subsectionTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#555",
    marginBottom: 8,
  },
  row: {
    marginBottom: 12,
  },
  switchRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: "500",
    color: "#555",
    marginBottom: 4,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 4,
    padding: 8,
    fontSize: 14,
    backgroundColor: "#fff",
  },
  multilineInput: {
    height: 80,
    textAlignVertical: "top",
  },
  corsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 4,
  },
  corsOrigin: {
    flex: 1,
    fontSize: 14,
    color: "#333",
  },
  removeButton: {
    color: "#ff4444",
    fontWeight: "500",
  },
  pickerContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 4,
  },
  pickerOption: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: "#ddd",
    backgroundColor: "#f5f5f5",
  },
  pickerOptionSelected: {
    backgroundColor: "#0066cc",
    borderColor: "#0066cc",
  },
  pickerOptionText: {
    fontSize: 12,
    color: "#333",
  },
  pickerOptionTextSelected: {
    color: "white",
  },
  button: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 4,
    alignItems: "center",
  },
  primaryButton: {
    backgroundColor: "#0066cc",
  },
  secondaryButton: {
    backgroundColor: "#6c757d",
  },
  warningButton: {
    backgroundColor: "#ffc107",
  },
  disabledButton: {
    backgroundColor: "#ccc",
  },
  buttonText: {
    color: "white",
    fontWeight: "500",
  },
  saveContainer: {
    padding: 16,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: "white",
  },
  modalHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: "bold",
  },
  closeButton: {
    color: "#0066cc",
    fontSize: 16,
  },
  rawEditor: {
    flex: 1,
    margin: 16,
    padding: 12,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 4,
    fontFamily: "monospace",
    fontSize: 12,
    textAlignVertical: "top",
  },
  modalActions: {
    padding: 16,
  },
});
