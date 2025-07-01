import { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";

const API_URL = "http://localhost:8000/config";
