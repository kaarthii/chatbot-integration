package com.example.ChatBot.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.ChatBot.model.ChatHistory;
import com.example.ChatBot.model.ChatSession;

public interface ChatSessionRepository extends JpaRepository<ChatSession, String>{
	List<ChatHistory> findByUserId(String userId);


}
