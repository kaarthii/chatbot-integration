package com.example.ChatBot.model;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class ChatSession {
	@Id 
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	@Column(name = "session_id")
    private String sessionId;
	@Column(name = "user_id")
	private String userId;
	
	@Column(name = "session_name")
	private String sessionName;
	private LocalDateTime created_at=LocalDateTime.now();

}
