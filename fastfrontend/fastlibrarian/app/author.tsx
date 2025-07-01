import { useEffect, useState, useCallback } from "react";
import { sharedStyles as styles } from "../app/sharedstyles";
import BookCard from "../app/BookCard";

import { useLocalSearchParams, useRouter } from "expo-router";
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  Pressable,
  ScrollView,
} from "react-native";

const API_URL = "http://localhost:8000/authors";

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
  status?: BookStatus | null; // E-book status
  a_status?: BookStatus | null; // Audio book status
  p_status?: BookStatus | null; // Physical book status
  description: string | null;
  external_refs: Record<string, any> | null;
  authors?: { id: string; name: string }[];
  series?: { id: string; name: string }[] | { id: string; name: string } | null;
}

interface Author {
  id: string;
  name: string;
  bio: string | null;
  external_refs: Record<string, any> | null;
  books: Book[];
}

export default function AuthorScreen() {
  const { id } = useLocalSearchParams();

  const [author, setAuthor] = useState<Author | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  const fetchAuthor = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      if (!id) {
        setError("Author ID is missing");
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_URL}/${id}`);

      if (!response.ok) {
        throw new Error(`Error fetching author: ${response.statusText}`);
      }

      const data = await response.json();
      setAuthor(data);
    } catch (err) {
      console.error("Failed to fetch author:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch author");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchAuthor();
  }, [fetchAuthor]);

  const updateAuthorBooks = async () => {
    try {
      setUpdating(true);
      setError(null);

      const response = await fetch(
        `${API_URL}/update_single_author_books/${id}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(`Error updating author books: ${response.statusText}`);
      }

      const data = await response.json();
      setAuthor(data);
    } catch (err) {
      console.error("Failed to update author books:", err);
      setError(
        err instanceof Error ? err.message : "Failed to update author books"
      );
    } finally {
      setUpdating(false);
    }
  };

  const updateBookStatus = async (
    bookId: string,
    type: "ebook" | "audio" | "physical",
    status: BookStatus
  ) => {
    try {
      const statusField =
        type === "ebook"
          ? "status"
          : type === "audio"
          ? "a_status"
          : "p_status";
      await fetch(`http://localhost:8000/books/${bookId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          [statusField]: status,
        }),
      });
      // Refresh the author data to show updated status
      fetchAuthor();
    } catch (error) {
      console.error("Failed to update book status:", error);
    }
  };

  if (loading) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: "center", alignItems: "center" },
        ]}
      >
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={{ marginTop: 16 }}>Loading author details...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: "center", alignItems: "center" },
        ]}
      >
        <Text style={{ color: "red", marginBottom: 16 }}>{error}</Text>
        <Pressable
          style={[{ backgroundColor: "#007AFF", padding: 12, borderRadius: 8 }]}
          onPress={() => fetchAuthor()}
        >
          <Text style={{ color: "white" }}>Retry</Text>
        </Pressable>
      </View>
    );
  }

  if (!author) {
    return (
      <View
        style={[
          styles.container,
          { justifyContent: "center", alignItems: "center" },
        ]}
      >
        <Text>Author not found</Text>
        <Pressable
          style={[
            {
              backgroundColor: "#007AFF",
              padding: 12,
              borderRadius: 8,
              marginTop: 16,
            },
          ]}
          onPress={() => router.back()}
        >
          <Text style={{ color: "white" }}>Go Back</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={{ alignItems: "center", marginBottom: 24 }}>
        <Text style={styles.title}>{author.name}</Text>
        {author.external_refs?.hardcover_id && (
          <Text style={styles.tertiaryText}>
            Hardcover ID: {author.external_refs.hardcover_id}
          </Text>
        )}
      </View>

      {author.bio && (
        <View style={styles.card}>
          <Text style={styles.primaryName}>Biography</Text>
          <Text style={styles.primaryText}>{author.bio}</Text>
        </View>
      )}

      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          marginVertical: 16,
        }}
      >
        <Text style={styles.subtitle}>Books ({author.books.length})</Text>
        <Pressable
          style={[{ backgroundColor: "#007AFF", padding: 10, borderRadius: 8 }]}
          onPress={updateAuthorBooks}
          disabled={updating}
        >
          <Text style={{ color: "white" }}>
            {updating ? "Updating..." : "Refresh Books"}
          </Text>
        </Pressable>
      </View>

      {author.books.length === 0 ? (
        <View style={styles.card}>
          <Text style={styles.primaryText}>
            No books found for this author.
          </Text>
        </View>
      ) : (
        <FlatList
          data={author.books}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <BookCard
              book={item}
              showDetailsButton
              onPressDetails={() =>
                router.navigate({ pathname: "/book", params: { id: item.id } })
              }
              onStatusChange={(type, status) =>
                updateBookStatus(item.id, type, status)
              }
              containerStyle={{ marginBottom: 12 }}
            />
          )}
          scrollEnabled={false}
          style={{ marginBottom: 20 }}
        />
      )}
    </ScrollView>
  );
}
