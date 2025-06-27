import { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";

const API_URL = "http://localhost:8000/series";

export default function SeriesScreen() {
  const [series, setSeries] = useState([]);
  const [name, setName] = useState("");

  const fetchSeries = async () => {
    const res = await fetch(API_URL);
    setSeries(await res.json());
  };

  const createSeries = async () => {
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    setName("");
    fetchSeries();
  };

  useEffect(() => { fetchSeries(); }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Series</Text>
      <FlatList
        data={series}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.name} - {item.description}</Text>
        )}
      />
      <Text style={styles.subtitle}>Add Series</Text>
      <TextInput placeholder="Name" value={name} onChangeText={setName} style={styles.input} />
      <Button title="Create" onPress={createSeries} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24 },
  title: { fontSize: 28, marginBottom: 16 },
  subtitle: { fontSize: 20, marginTop: 24 },
  input: { borderWidth: 1, borderColor: "#ccc", marginVertical: 8, padding: 8, borderRadius: 4 },
  item: { fontSize: 16, marginVertical: 4 },
});
