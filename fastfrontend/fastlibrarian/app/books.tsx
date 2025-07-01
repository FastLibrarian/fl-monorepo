import { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";
import BookCard from "../app/BookCard";

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
  description?: string | null;
  authors?: { id: string; name: string }[];
  series?: { id: string; name: string }[] | { id: string; name: string } | null;
  status?: BookStatus | null; // E-book status
  a_status?: BookStatus | null; // Audio book status
  p_status?: BookStatus | null; // Physical book status
}

export default function BooksScreen() {
  const [books, setBooks] = useState<Book[]>([]);
  const [title, setTitle] = useState("");
  const [author_id, setAuthorId] = useState("");
  const [description, setDescription] = useState("");
  const [series_id, setSeriesId] = useState("");
  const [adding, setAdding] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<{
    bookId: string;
    type: string;
  } | null>(null);

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
      await fetch(`${API_URL}/${bookId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          [statusField]: status,
        }),
      });
      // Close dropdown and refresh
      setActiveDropdown(null);
      fetchBooks();
    } catch (error) {
      console.error("Failed to update book status:", error);
    }
  };

  const handleDropdownToggle = (bookId: string, type: string) => {
    if (activeDropdown?.bookId === bookId && activeDropdown?.type === type) {
      setActiveDropdown(null);
    } else {
      setActiveDropdown({ bookId, type });
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
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <BookCard
            book={item}
            onStatusChange={(type, status) =>
              updateBookStatus(item.id, type, status)
            }
            activeDropdown={activeDropdown}
            onDropdownToggle={handleDropdownToggle}
          />
        )}
      />
      <Text style={styles.subtitle}>Add Book</Text>
      <TextInput
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
        style={styles.textInput}
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
