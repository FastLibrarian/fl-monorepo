import { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";

const API_URL = "http://localhost:8000/books";

export default function BooksScreen() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState("");
  const [author_id, setAuthorId] = useState("");
  const [description, setDescription] = useState("");
  const [series_id, setSeriesId] = useState("");
  const [adding, setAdding] = useState(false);

  const fetchBooks = async () => {
    const res = await fetch(API_URL);
    setBooks(await res.json());
  };

  const addBook = async () => {
    setAdding(true);
    try {
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
    } catch (error) {
      console.error(error);
    } finally {
      setAdding(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Books</Text>
      <FlatList
        data={books}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.primaryName}>{item.title}</Text>
            {/* Display all author names, comma separated */}
            <Text style={styles.secondaryName}>
              {item.authors && item.authors.length > 0
                ? item.authors.map((a) => a.name).join(", ")
                : "(No authors)"}
            </Text>
            {item.description ? (
              <Text style={styles.primaryText}>{item.description}</Text>
            ) : (
              <Text style={styles.tertiaryText}>(No description)</Text>
            )}
            {/* Display all series names, comma separated */}
            {item.series && item.series.length > 0 ? (
              <Text style={styles.secondaryName}>
                Series: {item.series.map((s) => s.name).join(", ")}
              </Text>
            ) : null}
          </View>
        )}
      />
      <Text style={styles.subtitle}>Add Book</Text>
      <TextInput
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
        style={styles.input}
      />

      <View
        style={{
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Button
          title={adding ? "Adding..." : "Add Book"}
          onPress={addBook}
          disabled={adding}
        />
      </View>
    </View>
  );
}
