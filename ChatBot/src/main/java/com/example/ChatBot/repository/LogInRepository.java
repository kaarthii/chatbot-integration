package com.example.ChatBot.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.ChatBot.model.LogIn;

public interface LogInRepository extends JpaRepository<LogIn,Long>{
	LogIn findByUserNameAndPassword(String userName, String password);
	LogIn findBySessionId(String sessionId);

}
