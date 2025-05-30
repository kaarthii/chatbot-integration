package com.example.ChatBot.model;

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
public class LogIn {
	@Id 
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	
	@Column(name = "user_id")
	private String userId;
	@Column(name = "session_id")
    private String sessionId;
	private String password;
	@Column(name = "user_name")
	private String userName;


}
