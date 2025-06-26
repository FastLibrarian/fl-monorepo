import { useEffect, useState } from "react";
// Import React hooks for state and lifecycle management.

import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
// Import React Native components for UI layout, text, input, button, list, and styling.

const API_URL = "http://localhost:8000/authors";
// The base URL for the authors API endpoint.
const FIND_AUTHORS_URL = API_URL + "/find_authors";
// The base URL for the find authors API endpoint.

export default function AuthorsScreen() {
  // Define the main functional component for the Authors screen.

  const [authors, setAuthors] = useState([]);
  // State to hold the list of authors fetched from the API.

  const [name, setName] = useState("");
  // State for the new author's name input field.

  const [foundAuthors, setFoundAuthors] = useState([]);
  // State to hold the list of found authors from the search.

  const [searching, setSearching] = useState(false);
  // State to manage the searching status for better UX.

  const fetchAuthors = async () => {
    // Async function to fetch the list of authors from the backend.
    const res = await fetch(API_URL);
    setAuthors(await res.json());
    // Fetches data and updates the authors state.
  };

  const findAuthors = async () => {
    // Async function to find authors via the FIND_AUTHORS_URL.
    setSearching(true);
    try {
      const res = await fetch(FIND_AUTHORS_URL + "?" + new URLSearchParams({ name: name }), {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setFoundAuthors(data);
      // On successful response, update the foundAuthors state.
    } catch (error) {
      console.error(error);
      // Log any error for debugging.
    } finally {
      setSearching(false);
    }
  };

  useEffect(() => { fetchAuthors(); }, []);
  // useEffect runs fetchAuthors once when the component mounts.

  return (
    <View style={styles.container}>
      {/* Main container for the page */}
      <Text style={styles.title}>Authors</Text>
      {/* Page title */}
      <FlatList
        data={authors}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.name} - {item.bio}</Text>
        )}
      />
      {/* FlatList displays the list of authors. Each item shows name and bio. */}
      {/* --- Find Authors Section --- */}
      <Text style={styles.subtitle}>Find Authors</Text>
      {/* Subtitle for the find authors section */}
      <TextInput
        placeholder="Name"
        value={name}
        onChangeText={setName}
        style={styles.input}
      />
      {/* Input field for searching authors by name */}
      <Button title={searching ? "Searching..." : "Find"} onPress={findAuthors} disabled={searching} />
      {/* Button to submit the author search */}
      <FlatList
        data={foundAuthors}
        keyExtractor={(item, idx) => (item.id ? item.id.toString() : "ext_" + idx)}
        renderItem={({ item }) => (
          <Text style={styles.item}>
            {item.name} - {item.bio} {item.in_db ? "(in DB)" : "(external)"}
          </Text>
        )}
        ListEmptyComponent={foundAuthors.length === 0 && name ? <Text style={styles.item}>No authors found.</Text> : null}
      />
      {/* FlatList displays the list of found authors. Indicates if the author is in the database or external. */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24 },
  // Styles for the main container
  title: { fontSize: 28, marginBottom: 16 },
  // Styles for the page title
  subtitle: { fontSize: 20, marginTop: 24 },
  // Styles for the subtitle
  input: { borderWidth: 1, borderColor: "#ccc", marginVertical: 8, padding: 8, borderRadius: 4 },
  // Styles for text inputs
  item: { fontSize: 16, marginVertical: 4 },
  // Styles for list items
});
