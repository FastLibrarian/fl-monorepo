import { use, useEffect, useState } from "react";
import { sharedStyles as styles } from "../app/sharedstyles";

import { useLocalSearchParams, useRouter } from "expo-router";
import {
  View,
  Button,
  Text,
  FlatList,
  ActivityIndicator,
  Pressable,
  ScrollView,
} from "react-native";

const API_URL = "http://localhost:8000/books";

// Book status enum matching the API
enum BookStatus {
  Wanted = "Wanted",
  Have = "Have",
  Ignored = "Ignored",
  Delete = "Delete",
}

interface Book {
  id: string;
  title: string;
  description: string | null;
  authors: { id: string; name: string }[];
  series: { id: string; name: string }[] | null;
  external_refs: Record<string, any> | null;
  status?: BookStatus | null; // E-book status
  a_status?: BookStatus | null; // Audio book status
  p_status?: BookStatus | null; // Physical book status
}

export default function BookScreen() {
  const { id } = useLocalSearchParams();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBook();
  }, [id]);
  const router = useRouter();
  const fetchBook = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!id) {
        setError("Book ID is missing");
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_URL}/${id}`);

      if (!response.ok) {
        throw new Error(`Error fetching book: ${response.statusText}`);
      }

      const data = await response.json();
      setBook(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch book details");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.title}>Loading book details...</Text>
      </View>
    );
  }
  if (error) {
    return (
      <View style={styles.container}>
        <Text style={{ color: "red" }}>{error}</Text>
      </View>
    );
  }
  if (!book) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Book not found</Text>
      </View>
    );
  }
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{book.title}</Text>
      <Text style={styles.primaryText}>
        {book.description || "No description available"}
      </Text>
      <Text style={styles.subtitle}>Author(s):</Text>
      <FlatList
        data={book.authors}
        keyExtractor={(author) => author.id}
        renderItem={({ item }) => (
          <Pressable
            onPress={() =>
              router.navigate({
                pathname: "/author",
                params: { id: item.id },
              })
            }
          >
            <Text style={styles.primaryName}>{item.name}</Text>
          </Pressable>
        )}
      />
      <Text style={styles.subtitle}>Series:</Text>
      <FlatList
        data={book.series}
        keyExtractor={(series) => series.id}
        renderItem={({ item }) => (
          <Pressable
            onPress={() =>
              router.navigate({
                pathname: "/single_series",
                params: { id: item.id },
              })
            }
          >
            <Text style={styles.primaryName}>{item.name}</Text>
          </Pressable>
        )}
      />
      {book.external_refs && (
        <View>
          <Text style={styles.subtitle}>External References:</Text>
          {Object.entries(book.external_refs).map(([key, value]) => (
            <Text key={key} style={styles.secon}>
              {key}: {value}
            </Text>
          ))}
        </View>
      )}

      <Button title="Go Back" onPress={() => router.back()} />
    </ScrollView>
  );
}
