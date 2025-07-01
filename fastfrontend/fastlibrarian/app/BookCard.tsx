import React, { useState } from "react";
import {
  View,
  Text,
  Pressable,
  StyleProp,
  ViewStyle,
  Modal,
  TouchableOpacity,
} from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";
import { useRouter } from "expo-router";

// Book status enum matching the API
enum BookStatus {
  Wanted = "Wanted",
  Have = "Have",
  Ignored = "Ignored",
  Delete = "Delete",
}

interface BookCardProps {
  book: {
    id: string;
    title: string;
    description?: string | null;
    authors?: { id: string; name: string }[];
    series?:
      | { id: string; name: string }[]
      | { id: string; name: string }
      | null;
    status?: BookStatus | null; // E-book status
    a_status?: BookStatus | null; // Audio book status
    p_status?: BookStatus | null; // Physical book status
  };
  onPressDetails?: () => void;
  showDetailsButton?: boolean;
  containerStyle?: StyleProp<ViewStyle>;
  onStatusChange?: (
    type: "ebook" | "audio" | "physical",
    status: BookStatus
  ) => void;
}

// Status Dropdown Component
const StatusDropdown: React.FC<{
  label: string;
  value: BookStatus | null;
  onValueChange: (status: BookStatus) => void;
}> = ({ label, value, onValueChange }) => {
  const [modalVisible, setModalVisible] = useState(false);

  const statusOptions = Object.values(BookStatus);

  return (
    <View style={{ marginVertical: 4 }}>
      <Text style={[styles.tertiaryText, { fontSize: 12 }]}>{label}:</Text>
      <Pressable
        onPress={() => setModalVisible(true)}
        style={{
          borderWidth: 1,
          borderColor: "#ccc",
          borderRadius: 4,
          paddingHorizontal: 8,
          paddingVertical: 4,
          backgroundColor: "#f9f9f9",
          minHeight: 32,
          justifyContent: "center",
        }}
      >
        <Text style={[styles.primaryText, { fontSize: 14 }]}>
          {value || "Select status"}
        </Text>
      </Pressable>

      <Modal
        visible={modalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalVisible(false)}
      >
        <TouchableOpacity
          style={{
            flex: 1,
            backgroundColor: "rgba(0,0,0,0.5)",
            justifyContent: "center",
            alignItems: "center",
          }}
          onPress={() => setModalVisible(false)}
        >
          <View
            style={{
              backgroundColor: "white",
              borderRadius: 8,
              padding: 16,
              minWidth: 200,
              maxWidth: 300,
            }}
          >
            <Text
              style={[
                styles.primaryName,
                { marginBottom: 12, textAlign: "center" },
              ]}
            >
              Select {label}
            </Text>
            {statusOptions.map((status) => (
              <Pressable
                key={status}
                onPress={() => {
                  onValueChange(status);
                  setModalVisible(false);
                }}
                style={{
                  paddingVertical: 12,
                  paddingHorizontal: 16,
                  borderBottomWidth: 1,
                  borderBottomColor: "#eee",
                }}
              >
                <Text
                  style={[
                    styles.primaryText,
                    value === status && {
                      fontWeight: "bold",
                      color: "#007AFF",
                    },
                  ]}
                >
                  {status}
                </Text>
              </Pressable>
            ))}
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
};

const BookCard: React.FC<BookCardProps> = ({
  book,
  onPressDetails,
  showDetailsButton = true,
  containerStyle,
  onStatusChange,
}) => {
  const router = useRouter();

  // Debug: Log status values
  console.log("Book statuses for", book.title, ":", {
    status: book.status,
    a_status: book.a_status,
    p_status: book.p_status,
  });

  // Support both array and single object for series
  const seriesList = Array.isArray(book.series)
    ? book.series
    : book.series
    ? [book.series]
    : [];

  const handlePress = onPressDetails
    ? onPressDetails
    : () => router.navigate({ pathname: "/book", params: { id: book.id } });

  const handleStatusChange = (
    type: "ebook" | "audio" | "physical",
    status: BookStatus
  ) => {
    if (onStatusChange) {
      onStatusChange(type, status);
    }
  };

  return (
    <View style={[styles.card, containerStyle]}>
      <Text style={styles.primaryName}>{book.title}</Text>
      {book.authors && book.authors.length > 0 && (
        <Text style={styles.secondaryName}>
          {book.authors.map((a) => a.name).join(", ")}
        </Text>
      )}
      {book.description ? (
        <Text style={styles.primaryText}>{book.description}</Text>
      ) : (
        <Text style={styles.tertiaryText}>(No description)</Text>
      )}
      {seriesList.length > 0 && (
        <Text style={styles.secondaryName}>
          Series: {seriesList.map((s) => s.name).join(", ")}
        </Text>
      )}

      {/* Status Dropdowns */}
      <View style={{ marginTop: 12 }}>
        <StatusDropdown
          label="E-book Status"
          value={book.status || null}
          onValueChange={(status) => handleStatusChange("ebook", status)}
        />
        <StatusDropdown
          label="Audiobook Status"
          value={book.a_status || null}
          onValueChange={(status) => handleStatusChange("audio", status)}
        />
        <StatusDropdown
          label="Physical Book Status"
          value={book.p_status || null}
          onValueChange={(status) => handleStatusChange("physical", status)}
        />
      </View>

      {showDetailsButton && (
        <Pressable
          onPress={handlePress}
          style={{ alignSelf: "flex-end", marginTop: 8 }}
        >
          <Text style={styles.addButton}>View Details</Text>
        </Pressable>
      )}
    </View>
  );
};

export default BookCard;
