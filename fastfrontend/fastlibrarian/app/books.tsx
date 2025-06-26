import { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";

const API_URL = "http://localhost:8000/books";

export default function BooksScreen() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState("");
  const [author_id, setAuthorId] = useState("");
  const [description, setDescription] = useState("");
  const [series_id, setSeriesId] = useState("");

  const fetchBooks = async () => {
    const res = await fetch(API_URL);
    setBooks(await res.json());
  };

  const searchBook = async () => {
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        author_id: Number(author_id),
        description,
        series_id: series_id ? Number(series_id) : null,
      }),
    });
    setTitle("");
    setAuthorId("");
    setDescription("");
    setSeriesId("");
    fetchBooks();
  };

  useEffect(() => { fetchBooks(); }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Books</Text>
      <FlatList
        data={books}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.title} (Author {item.author_id})</Text>
        )}
      />
      <Text style={styles.subtitle}>Add Book</Text>
      <TextInput placeholder="Title" value={title} onChangeText={setTitle} style={styles.input} />

      <Button title="Search" onPress={searchBook} />
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
