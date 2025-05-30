package com.example.ChatBot.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.ChatBot.model.ChatSession;
import com.example.ChatBot.model.ChatHistory;

public interface ChatHistoryRepository extends JpaRepository<ChatHistory,Long> {

	List<ChatHistory> findBySessionId(String sessionId);

}
