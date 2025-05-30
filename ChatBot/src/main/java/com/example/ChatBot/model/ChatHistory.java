package com.example.ChatBot.model;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
@Entity
@Getter
@Setter
public class ChatHistory {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Column(name = "user_id")
	private String userId;
	@Column(name = "session_id")
    private String sessionId;
	private String question;
	@Column(name = "answer", columnDefinition = "TEXT")
	private String answer;
	private LocalDateTime timestamp=LocalDateTime.now();
	


}
