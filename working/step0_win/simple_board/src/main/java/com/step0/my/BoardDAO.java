package com.step0.my;

import java.awt.List;

import javax.servlet.http.HttpSession;

public interface BoardDAO {
	public void create(BoardVO vo) throws Excetion;
	public BoardVO read(int bno) throws Excetion;
	public void update(BoardVO vo) throws Excetion;
	public void delete(int bno) throws Excetion;
	public List <BoardVO> listAll(int bno, HttpSession session) throws Excetion;
}
