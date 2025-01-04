from TrackRequirements import *

from TestVictoryCommon import *


class TestAcquiredCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = AcquiredCities(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AcquiredCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AcquiredCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_city_acquired(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Acquired cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_city_built(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Acquired cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_same_city_twice(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityBuilt", city)
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Acquired cities: 1 / 2")
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)
	

class TestBrokeredPeace(ExtendedTestCase):

	def setUp(self):
		self.requirement = BrokeredPeace(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BrokeredPeace(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BrokeredPeace(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_peace_brokered(self):
		events.fireEvent("peaceBrokered", self.iPlayer, 1, 2)
		events.fireEvent("peaceBrokered", self.iPlayer, 1, 2)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Peace deals brokered: 2 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_peace_brokered_other(self):
		events.fireEvent("peaceBrokered", 1, 2, 3)
		events.fireEvent("peaceBrokered", 1, 2, 3)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Peace deals brokered: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_peace_brokered_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("peaceBrokered", 0, 2, 3)
			events.fireEvent("peaceBrokered", 1, 4, 5)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Peace deals brokered: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestCelebrateTurns(ExtendedTestCase):

	def setUp(self):
		self.requirement = CelebrateTurns(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CelebrateTurns(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CelebrateTurns(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "your cities celebrate for two turns")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns of celebration: 0 / 2")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_fewer(self):
		city = TestCities.one()
		city.setWeLoveTheKingDay(True)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns of celebration: 1 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_more(self):
		city1, city2 = cities = TestCities.num(2)
		city1.setWeLoveTheKingDay(True)
		city2.setWeLoveTheKingDay(True)
		
		try:
			for iTurn in range(2):
				events.fireEvent("BeginPlayerTurn", iTurn, self.iPlayer)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Turns of celebration: 4 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_other_owner(self):
		city = TestCities.one(1)
		city.setWeLoveTheKingDay(True)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 0)
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns of celebration: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		city.setWeLoveTheKingDay(True)
		
		try:
			for iTurn in range(2):
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Turns of celebration: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestCityCaptureGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityCaptureGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.city = TestCities.one(1)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
		self.city.kill()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityCaptureGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityCaptureGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold from conquering cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_city_capture_gold(self):
		events.fireEvent("cityCaptureGold", self.city, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from conquering cities: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_city_capture_gold_other(self):
		events.fireEvent("cityCaptureGold", self.city, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from conquering cities: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("cityCaptureGold", self.city, 1, 100)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from conquering cities: 100 / 100")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestCombatFood(ExtendedTestCase):

	def setUp(self):
		self.requirement = CombatFood(10)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CombatFood(10)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CombatFood(10)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "10 food from combat")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("combatFood", 0, unit, 5)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Food from combat: 5 / 10")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
	
	def test_more(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("combatFood", 0, unit, 20)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 20)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Food from combat: 20 / 10")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
	
	def test_different_player(self):
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("combatFood", 1, unit, 10)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Food from combat: 0 / 10")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("combatFood", 1, unit, 10)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 10)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Food from combat: 10 / 10")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestConqueredCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = ConqueredCities(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ConqueredCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ConqueredCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_record_conquered(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_peacefully_acquired(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, False, True)
			events.fireEvent("cityAcquired", 1, 0, city2, False, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 0, 1, city1, True, False)
			events.fireEvent("cityAcquired", 0, 1, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_owner_changes_after_conquest(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
			
	def test_city_destroyed_after_conquest(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
			
			city2.kill()
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 1 / 2")
		finally:
			city1.kill()
	
	def test_conquered_but_not_controlled(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
			
			player(1).acquireCity(city1, False, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 1 / 2")
		finally:
			TestCities.city(0).kill()
			city2.kill()
	
	def test_conquered_control_not_required(self):
		requirement = ConqueredCities(2, bControl=False).create()
		requirement.register_handlers(self.goal)
	
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(requirement.evaluate(self.evaluator), 2)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
			
			player(1).acquireCity(city1, False, True)
			
			self.assertEqual(requirement.evaluate(self.evaluator), 2)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
		finally:
			TestCities.city(0).kill()
			city2.kill()
			requirement.deregister_handlers()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestConqueredCitiesInside(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Test Area")
		self.requirement = ConqueredCities(2, inside=self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_conquer_in_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities in Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_conquer_not_in_area(self):
		_, _, city1, city2 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities in Test Area: 0 / 2")
		finally:
			cities.kill()


class TestConqueredCitiesOutside(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().all().without([(57, 35), (59, 35)]).named("Test Area")
		self.requirement = ConqueredCities(2, outside=self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities outside of Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"outside of Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "outside of Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_conquer_outside_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities outside of Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_conquer_not_in_area(self):
		_, _, city1, city2 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities outside of Test Area: 0 / 2")
		finally:
			cities.kill()


class TestConqueredCitiesCivs(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsArgument(1).named("Test Civs")
		self.requirement = ConqueredCities(2, civs=self.civs).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Test Civs cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_conquer_of_civ(self):
		city1, city2 = TestCities.owners(1, 1)
		
		try:
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(cities.owner(0).count(), 2)
			self.assertEqual(len(self.requirement.recorded), 2)
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered Test Civs cities: 2 / 2")
		finally:
			TestCities.city(0).kill()
			TestCities.city(1).kill()
	
	def test_conquer_not_of_civ(self):
		city1, city2 = cities = TestCities.owners(2, 2)
		
		try:
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered Test Civs cities: 0 / 2")
		finally:
			TestCities.city(0).kill()
			TestCities.city(1).kill()


class TestConstructed(ExtendedTestCase):

	def setUp(self):
		self.requirement = Constructed(iMarket, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Constructed(Market, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Constructed(Market, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Markets")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 0 / 2")
	
	def test_less(self):
		city = TestCities.one()
	
		events.fireEvent("buildingBuilt", city, iMarket)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 1 / 2")
		finally:
			city.kill()
	
	def test_more(self):
		cities = TestCities.num(3)
		
		for city in cities:
			events.fireEvent("buildingBuilt", city, iMarket)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Markets: 3 / 2")
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		
		events.fireEvent("buildingBuilt", city, iMarket)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 0 / 2")
		finally:
			city.kill()
	
	def test_different_building(self):
		cities = TestCities.num(3)
		
		for city in cities:
			events.fireEvent("buildingBuilt", city, iLibrary)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 0 / 2")
		finally:
			cities.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestDefeatedUnits(ExtendedTestCase):

	def setUp(self):
		self.requirement = DefeatedUnits(CivsArgument(iBabylonia), 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.our_unit = makeUnit(0, iSwordsman, (10, 10))
		self.their_unit = makeUnit(1, iSwordsman, (11, 11))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
		self.our_unit.kill(False, -1)
		self.their_unit.kill(False, -1)
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "DefeatedUnits(Babylonia, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "DefeatedUnits(Babylonia, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Babylonian units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Defeated Babylonian units: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_less(self):
		events.fireEvent("combatResult", self.our_unit, self.their_unit)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Defeated Babylonian units: 1 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_more(self):
		for _ in range(3):
			events.fireEvent("combatResult", self.our_unit, self.their_unit)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Defeated Babylonian units: 3 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_defeat(self):
		for _ in range(3):
			events.fireEvent("combatResult", self.their_unit, self.our_unit)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Defeated Babylonian units: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_civilization(self):
		other_unit = makeUnit(2, iSwordsman, (9, 9))
		
		try:
			for _ in range(3):
				events.fireEvent("combatResult", self.our_unit, other_unit)
				
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Defeated Babylonian units: 0 / 2")
			self.assertEqual(self.goal.checked, False)
		finally:
			other_unit.kill(False, -1)

	def test_not_checked_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestEnslaveCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = EnslaveCount(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "EnslaveCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "EnslaveCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_enslave(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved units: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_minor(self):
		unit = makeUnit(iNative, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved units: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_other(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 2, unit)
			events.fireEvent("enslave", 2, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved units: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 1, unit)
			events.fireEvent("enslave", 1, unit)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved units: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)
		
		
class TestEnslaveCountExcluding(ExtendedTestCase):

	def setUp(self):
		self.requirement = EnslaveCount(2, excluding=CivsArgument(1).named("Test Civs")).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Test Civs units")
	
	def test_enslave_excluded(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved Test Civs units: 0 / 2")
		finally:
			unit.kill(False, -1)
	
	def test_enslave_not_excluded(self):
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved Test Civs units: 2 / 2")
		finally:
			unit.kill(False, -1)


class TestEraFirstDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = EraFirstDiscover(iClassical, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "EraFirstDiscover(Classical, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "EraFirstDiscover(Classical, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Classical era technologies")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (21 remaining)")
		self.assertEqual(self.goal.checked, False)
	
	def test_fewer(self):
		team(0).setHasTech(iLaw, True, 0, True, False)
	
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
	
	def test_more(self):
		lTechs = [iLaw, iCurrency, iPhilosophy]
		for iTech in lTechs:
			team(0).setHasTech(iTech, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical technologies discovered first: 3 / 2 (18 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iTech in lTechs:
				team(0).setHasTech(iTech, False, 0, True, False)
	
	def test_other(self):
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
	
	def test_after_other(self):
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
			team(0).setHasTech(iLaw, False, 0, True, False)
	
	def test_different_era(self):
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (21 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(0).setHasTech(iFeudalism, False, 0, True, False)
	
	def test_not_enough_remaining(self):
		requirement = EraFirstDiscover(iClassical, 20)
		requirement.register_handlers(self.goal)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 20 (20 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iCurrency, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 20 (19 remaining)")
			self.assertEqual(self.goal.failed, True)
		finally:
			for iTech in [iLaw, iCurrency]:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_not_enough_remaining_with_discovered(self):
		requirement = EraFirstDiscover(iClassical, 20)
		requirement.register_handlers(self.goal)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (20 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iCurrency, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (19 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iPhilosophy, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (18 remaining)")
			self.assertEqual(self.goal.failed, True)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			for iTech in [iCurrency, iPhilosophy]:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		lTechs = [iLaw, iCurrency]
		for iTech in lTechs:
			team(1).setHasTech(iTech, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical technologies discovered first: 2 / 2 (19 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iTech in lTechs:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestGoldenAges(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldenAges(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GoldenAges(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GoldenAges(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Golden Ages")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_golden_age(self):
		for _ in range(8):
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
	
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden Ages: 0 / 2")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_golden_age(self):
		self.player.changeGoldenAgeTurns(1)
		
		try:
			for _ in range(16):
				events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 16)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Golden Ages: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			self.player.changeGoldenAgeTurns(-1)
	
	def test_golden_age_and_anarchy(self):
		self.player.changeGoldenAgeTurns(1)
		self.player.changeAnarchyTurns(1)
		
		try:
			for _ in range(8):
				events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden Ages: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			self.player.changeGoldenAgeTurns(-1)
			self.player.changeAnarchyTurns(-1)


class TestGreatGenerals(ExtendedTestCase):

	def setUp(self):
		self.requirement = GreatGenerals(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GreatGenerals(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GreatGenerals(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two great generals")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_great_general(self):
		city = TestCities.one()
		unit = makeUnit(0, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 0, city)
			events.fireEvent("greatPersonBorn", unit, 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great generals: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_different_unit(self):
		city = TestCities.one()
		unit = makeUnit(0, iGreatScientist, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 0, city)
			events.fireEvent("greatPersonBorn", unit, 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great generals: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_different_owner(self):
		city = TestCities.one(1)
		unit = makeUnit(1, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 1, city)
			events.fireEvent("greatPersonBorn", unit, 1, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great generals: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		unit = makeUnit(1, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 1, city)
			events.fireEvent("greatPersonBorn", unit, 1, city)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Great generals: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			unit.kill(False, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestHappiestTurns(ExtendedTestCase):

	def setUp(self):
		self.requirement = HappiestTurns(3).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "HappiestTurns(3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "HappiestTurns(3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the highest approval rating in the world for three turns")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_happiest(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.changeExtraHappiness(100)
		their_city.changeExtraHappiness(50)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 0)
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Turns at highest approval rating: 3 / 3")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_happiest_other(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.changeExtraHappiness(50)
		their_city.changeExtraHappiness(100)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 0)
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns at highest approval rating: 0 / 3")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		vassal_city.changeExtraHappiness(100)
		other_city.changeExtraHappiness(20)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
				events.fireEvent("BeginPlayerTurn", iTurn, 2)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Turns at highest approval rating: 3 / 3")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)


class TestHealthiestTurns(ExtendedTestCase):

	def setUp(self):
		self.requirement = HealthiestTurns(3).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "HealthiestTurns(3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "HealthiestTurns(3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the highest life expectancy rating in the world for three turns")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_healthiest(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.changeExtraHealth(100)
		their_city.changeExtraHealth(50)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 0)
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Turns at highest life expectancy: 3 / 3")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_healthiest_other(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.changeExtraHealth(50)
		their_city.changeExtraHealth(100)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 0)
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns at highest life expectancy: 0 / 3")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		vassal_city.changeExtraHealth(100)
		other_city.changeExtraHealth(20)
		
		try:
			for iTurn in range(3):
				events.fireEvent("BeginPlayerTurn", iTurn, 1)
				events.fireEvent("BeginPlayerTurn", iTurn, 2)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Turns at highest life expectancy: 3 / 3")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)


class TestImportCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ImportCount(iSilk, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ImportCount(Silk, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ImportCount(Silk, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Silk")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
	
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Imported Silk resources: 0 / 2")
	
	def test_less(self):
		player(self.iPlayer).changeBonusImport(iSilk, 1)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Imported Silk resources: 1 / 2")
		finally:
			player(self.iPlayer).changeBonusImport(iSilk, -1)
	
	def test_more(self):
		player(self.iPlayer).changeBonusImport(iSilk, 2)
		
		try:
			for _ in range(2):
				events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Imported Silk resources: 4 / 2")
		finally:
			player(self.iPlayer).changeBonusImport(iSilk, -2)
	
	def test_other_resource(self):
		player(self.iPlayer).changeBonusImport(iDye, 1)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Imported Silk resources: 0 / 2")
		finally:
			player(self.iPlayer).changeBonusImport(iDye, -1)


class TestPeaceTurns(ExtendedTestCase):

	def setUp(self):
		self.requirement = PeaceTurns(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PeaceTurns(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PeaceTurns(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "at peace for two turns")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_at_peace(self):
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 1, 0)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Turns at peace: 2 / 2")
	
	def test_at_war(self):
		team(0).setAtWar(1, True)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 0)
			events.fireEvent("BeginPlayerTurn", 1, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns at peace: 0 / 2")
		finally:
			team(0).setAtWar(1, False)
	

class TestPillageCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PillageCount(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.unit = makeUnit(self.iPlayer, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PillageCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PillageCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two improvements")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Improvements pillaged: 2 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Improvements pillaged: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
			events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Improvements pillaged: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestPiracyGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = PiracyGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.city = TestCities.one(1)
		self.unit = makeUnit(0, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
		self.city.kill()
		self.unit.kill(False, -1)
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PiracyGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PiracyGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold through piracy")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_unit_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_unit_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_blockade(self):
		events.fireEvent("blockade", 0, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_blockade_other(self):
		events.fireEvent("blockade", 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_combat_gold(self):
		events.fireEvent("combatGold", self.iPlayer, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_combat_gold_other(self):
		events.fireEvent("combatGold", 1, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("combatGold", 1, self.unit, 100)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestPopeTurns(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopeTurns(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopeTurns(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopeTurns(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the Pope for two turns")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_pope(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Turns as Pope: 0 / 2")
	
		self.assertEqual(self.goal.checked, False)


class TestProduction(ExtendedTestCase):

	def setUp(self):
		self.requirement = Production(10).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def teatDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Production(10)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Production(10)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "10 production")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		city = TestCities.one()

		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		try:
			self.assertEqual(city.getYieldRate(YieldTypes.YIELD_PRODUCTION), 3)
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Generated production: 3 / 10")
		finally:
			city.kill()
	
	def test_sufficient(self):
		city = TestCities.one()
		
		for _ in range(5):
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		try:
			self.assertEqual(city.getYieldRate(YieldTypes.YIELD_PRODUCTION), 3)
			self.assertEqual(self.requirement.evaluate(self.evaluator), 15)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Generated production: 15 / 10")
		finally:
			city.kill()
	
	def test_removed_forest(self):
		city = TestCities.one()
		plot = direction(city, DirectionTypes.DIRECTION_NORTH)
		
		plot.setFeatureType(iForest, 0)
		plot.setOwner(city.getOwner())
		
		events.fireEvent("plotFeatureRemoved", plot, city, iForest)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 20)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Generated production: 20 / 10")
		finally:
			city.kill()
			plot.setFeatureType(-1, -1)
			plot.setOwner(-1)
	
	def test_removed_savanna(self):
		city = TestCities.one()
		plot = direction(city, DirectionTypes.DIRECTION_NORTH)
		
		plot.setFeatureType(iSavanna, 0)
		plot.setOwner(city.getOwner())
		
		events.fireEvent("plotFeatureRemoved", plot, city, iSavanna)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Generated production: 0 / 10")
		finally:
			city.kill()
			plot.setFeatureType(-1, -1)
			plot.setOwner(-1)


class TestRaidGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = RaidGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.city = TestCities.one(1)
		self.unit = makeUnit(0, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
		self.city.kill()
		self.unit.kill(False, -1)
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "RaidGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "RaidGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by pillaging, conquering cities and sinking ships")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_unit_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_unit_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_city_capture_gold(self):
		events.fireEvent("cityCaptureGold", self.city, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_city_capture_gold_other(self):
		events.fireEvent("cityCaptureGold", self.city, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_combat_gold(self):
		events.fireEvent("combatGold", self.iPlayer, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_combat_gold_other(self):
		events.fireEvent("combatGold", 1, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("combatGold", 1, self.unit, 100)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestRazeCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = RazeCount(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "RazeCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "RazeCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_raze(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("cityRazed", city, 0)
			events.fireEvent("cityRazed", city, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Razed cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_raze_other(self):
		city = TestCities.one(2)
		
		try:
			events.fireEvent("cityRazed", city, 1)
			events.fireEvent("cityRazed", city, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Razed cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_raze_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(2)
		
		try:
			events.fireEvent("cityRazed", city, 1)
			events.fireEvent("cityRazed", city, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Razed cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestReligionSpreadCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligionSpreadCount(iBuddhism, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligionSpreadCount(Buddhism, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligionSpreadCount(Buddhism, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Buddhism to two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread: 0 / 2")
	
	def test_insufficient(self):
		unit = makeUnit(0, iBuddhistMissionary, (20, 20))
	
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread: 1 / 2")
		finally:
			unit.kill(-1, False)
	
	def test_sufficient(self):
		unit = makeUnit(0, iBuddhistMissionary, (20, 20))
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
				
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Buddhism spread: 2 / 2")
		finally:
			unit.kill(-1, False)
	
	def test_different_owner(self):
		unit = makeUnit(1, iBuddhistMissionary, (20, 20))
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread: 0 / 2")
		finally:
			unit.kill(-1, False)
	
	def test_different_religion(self):
		unit = makeUnit(0, iBuddhistMissionary, (20, 20))
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iHinduism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread: 0 / 2")
		finally:
			unit.kill(-1, False)
	
	def test_unsuccessful(self):
		unit = makeUnit(0, iBuddhistMissionary, (20, 20))
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread: 0 / 2")
		finally:
			unit.kill(-1, False)


class TestReligionSpreadPopulationCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligionSpreadPopulationCount(iBuddhism, 5).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligionSpreadPopulationCount(Buddhism, 5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligionSpreadPopulationCount(Buddhism, 5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Buddhism to a total population of five")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 0 / 5")
	
	def test_insufficient(self):
		city = TestCities.one()
		unit = makeUnit(0, iBuddhistMissionary, city)
		
		city.setPopulation(3)
	
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 3 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	
	def test_sufficient(self):
		city = TestCities.one()
		unit = makeUnit(0, iBuddhistMissionary, city)
		
		city.setPopulation(6)
		
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
				
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Buddhism spread population: 6 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	
	def test_no_city(self):
		unit = makeUnit(0, iBuddhistMissionary, (20, 20))
		
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 0 / 5")
		finally:
			unit.kill(-1, False)
	
	def test_two_cities(self):
		first_city, second_city = cities = TestCities.num(2)
		first_unit, second_unit = [makeUnit(0, iBuddhistMissionary, city) for city in cities]
		
		first_city.setPopulation(3)
		second_city.setPopulation(2)
		
		try:
			events.fireEvent("unitSpreadReligionAttempt", first_unit, iBuddhism, True)
			events.fireEvent("unitSpreadReligionAttempt", second_unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Buddhism spread population: 5 / 5")
		finally:
			cities.kill()
			first_unit.kill(-1, False)
			second_unit.kill(-1, False)
	
	def test_different_unit_owner(self):
		city = TestCities.one()
		unit = makeUnit(1, iBuddhistMissionary, city)
		
		city.setPopulation(6)
		
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 0 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	
	def test_different_city_owner(self):
		city = TestCities.one(1)
		unit = makeUnit(0, iBuddhistMissionary, city)
		
		city.setPopulation(6)
		
		try:
			events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Buddhism spread population: 6 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	
	def test_different_religion(self):
		city = TestCities.one()
		unit = makeUnit(0, iBuddhistMissionary, city)
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iHinduism, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 0 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	
	def test_unsuccessful(self):
		city = TestCities.one()
		unit = makeUnit(0, iBuddhistMissionary, city)
		
		try:
			for _ in range(2):
				events.fireEvent("unitSpreadReligionAttempt", unit, iBuddhism, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism spread population: 0 / 5")
		finally:
			unit.kill(-1, False)
			city.kill()
	

class TestResourceTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = ResourceTradeGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ResourceTradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ResourceTradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by selling resources")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_resource_trade_gold(self):
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trading resources: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
	
	def test_resource_trade_gold_other_player(self):
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trading resources: 0 / 100")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trading resources: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
			team(1).setVassal(0, False, False)


class TestSacrificeHappiness(ExtendedTestCase):

	def setUp(self):
		self.requirement = SacrificeGoldenAges(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SacrificeGoldenAges(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SacrificeGoldenAges(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two golden ages")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fewer(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("sacrificeGoldenAge", 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden ages from sacrificing slaves: 1 / 2")
		
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		
		try:
			for _ in range(3):
				events.fireEvent("sacrificeGoldenAge", 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Golden ages from sacrificing slaves: 3 / 2")

			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_different_player(self):
		city = TestCities.one(1)
		
		try:
			for _ in range(2):
				events.fireEvent("sacrificeGoldenAge", 1, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden ages from sacrificing slaves: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		
		try:
			for _ in range(2):
				events.fireEvent("sacrificeGoldenAge", 1, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Golden ages from sacrificing slaves: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestSettledCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = SettledCities(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SettledCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SettledCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_record_settled(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Settled cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_settled_then_lost(self):
		city1, city2 = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			player(1).acquireCity(city1, True, False)
			player(1).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
		finally:
			TestCities.city(0).kill()
			TestCities.city(1).kill()
	
	def test_conquered(self):
		city1, city2 = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
		finally:
			TestCities.city(0).kill()
			TestCities.city(1).kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestSettledCitiesArea(ExtendedTestCase):

	def setUp(self):
		self.requirement = SettledCities(2, area=AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Test Area")).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_settle_in_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Settled cities in Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_settle_not_in_area(self):
		city1, city2, city3, city4 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityBuilt", city3)
			events.fireEvent("cityBuilt", city4)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities in Test Area: 0 / 2")
		finally:
			cities.kill()


class TestSlaveTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = SlaveTradeGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SlaveTradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SlaveTradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold through the slave trade")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		events.fireEvent("playerSlaveTrade", 0, 50)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 50)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from slave trade: 50 / 100")
		
		self.assertEqual(self.goal.checked, True)
	
	def test_more(self):
		events.fireEvent("playerSlaveTrade", 0, 200)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 200)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from slave trade: 200 / 100")
		
		self.assertEqual(self.goal.checked, True)
	
	def test_other_player(self):
		events.fireEvent("playerSlaveTrade", 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from slave trade: 0 / 100")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("playerSlaveTrade", 1, 100)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from slave trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestSunkShips(ExtendedTestCase):

	def setUp(self):
		self.requirement = SunkShips(2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SunkShips(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SunkShips(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two enemy ships")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sink_enemy_ship(self):
		our_ship = makeUnit(0, iWarGalley, (3, 3))
		their_ship = makeUnit(1, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", our_ship, their_ship)
			events.fireEvent("combatResult", our_ship, their_ship)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enemy ships sunk: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			our_ship.kill(False, -1)
			their_ship.kill(False, -1)
	
	def test_sink_ship_other_player(self):
		their_ship = makeUnit(1, iWarGalley, (3, 3))
		other_ship = makeUnit(2, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", their_ship, other_ship)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enemy ships sunk: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			their_ship.kill(False, -1)
			other_ship.kill(False, -1)
	
	def test_defeat_land_unit(self):
		our_unit = makeUnit(0, iSwordsman, (61, 31))
		their_unit = makeUnit(1, iLightSwordsman, (62, 31))
		
		try:
			events.fireEvent("combatResult", our_unit, their_unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enemy ships sunk: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			our_unit.kill(False, -1)
			their_unit.kill(False, -1)
	
	def test_sink_enemy_ship_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		vassal_ship = makeUnit(1, iWarGalley, (3, 3))
		enemy_ship = makeUnit(2, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", vassal_ship, enemy_ship)
			events.fireEvent("combatResult", vassal_ship, enemy_ship)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Enemy ships sunk: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			vassal_ship.kill(False, -1)
			enemy_ship.kill(False, -1)
			
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = TradeGold(100).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tear_down(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "TradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by trade")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_player_gold_trade(self):
		events.fireEvent("playerGoldTrade", 1, 0, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
		
		self.assertEqual(self.goal.checked, True)
		
	def test_player_gold_trade_other(self):
		events.fireEvent("playerGoldTrade", 0, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_player_gold_trade_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("playerGoldTrade", 2, 1, 100)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_trade_mission(self):
		city = TestCities.one(1)
		events.fireEvent("tradeMission", iGreatMerchant, 0, city.getX(), city.getY(), 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_mission_other(self):
		city = TestCities.one()
		events.fireEvent("tradeMission", iGreatMerchant, 1, city.getX(), city.getY(), 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_trade_mission_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(2)
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 1, city.getX(), city.getY(), 100)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_deal(self):
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
	
	def test_trade_deal_other(self):
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
	
	def test_trade_deal_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
			team(1).setVassal(0, False, False)
	
	def test_trade_route(self):
		city1, city2 = cities = TestCities.num(2)
		
		plot(58, 35).setRouteType(iRouteRoad)
		
		player(0).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assertEqual(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			self.assertEqual(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			
			iExpectedCommerce = city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE)
			iExpectedCommerce *= player(0).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iExpectedCommerce /= 100
			
			self.assertEqual(iExpectedCommerce > 0, True)
			
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), iExpectedCommerce)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: %d / 100" % iExpectedCommerce)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).setCivics(iCivicsEconomy, iReciprocity)
			player(0).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
			
			plot(62, 31).setRouteType(-1)
			
			cities.kill()
			
	def test_trade_route_other(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		player(1).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assertEqual(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			self.assertEqual(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			
			events.fireEvent("BeginPlayerTurn", 0, 0)
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).setCivics(iCivicsEconomy, iReciprocity)
			player(1).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
			
			plot(62, 31).setRouteType(-1)
			
			cities.kill()


class TestTradeMissionCount(ExtendedTestCase):

	def setUp(self):
		self.city = LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City")
		self.requirement = TradeMissionCount(self.city, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "TradeMissionCount(Test City, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TradeMissionCount(Test City, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two trade missions to Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([(57, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		events.fireEvent("tradeMission", iGreatMerchant, 0, 57, 35, 1000)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade missions to Test City: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_trade_mission(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 0, 57, 35, 1000)
			events.fireEvent("tradeMission", iGreatMerchant, 0, 57, 35, 1000)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trade missions to Test City: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_mission_other_owner(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 0, 57, 35, 1000)
			events.fireEvent("tradeMission", iGreatMerchant, 0, 57, 35, 1000)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trade missions to Test City: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_mission_different_player(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 1, 57, 35, 1000)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade missions to Test City: 0 / 2")
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_trade_mission_different_city(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 0, 59, 35, 1000)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade missions to Test City: 0 / 2")
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)
			

test_cases = [
	TestAcquiredCities,
	TestBrokeredPeace,
	TestCelebrateTurns,
	TestCityCaptureGold,
	TestCombatFood,
	TestConqueredCities,
	TestConqueredCitiesInside,
	TestConqueredCitiesOutside,
	TestConqueredCitiesCivs,
	TestConstructed,
	TestDefeatedUnits,
	TestEnslaveCount,
	TestEnslaveCountExcluding,
	TestEraFirstDiscover,
	TestGoldenAges,
	TestGreatGenerals,
	TestHappiestTurns,
	TestHealthiestTurns,
	TestImportCount,
	TestPeaceTurns,
	TestPillageCount,
	TestPiracyGold,
	TestPopeTurns,
	TestProduction,
	TestRaidGold,
	TestRazeCount,
	TestReligionSpreadCount,
	TestReligionSpreadPopulationCount,
	TestResourceTradeGold,
	TestSacrificeHappiness,
	TestSettledCities,
	TestSettledCitiesArea,
	TestSlaveTradeGold,
	TestSunkShips,
	TestTradeGold,
	TestTradeMissionCount,
]