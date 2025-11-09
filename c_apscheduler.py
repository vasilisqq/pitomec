from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pets.pitomec import Pitomec
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from db.DAO import DAO
from bot.keyboards.inline import to_be_happy_btn, hungry_bttn, walk_bttn
from config import settings
from logger import logger
from typing import Optional

class C_scheduler():

    def __init__(self):
        logger.info("Инициализация планировщика задач")
        try:
            jobstores = {
                'default': RedisJobStore(
                    jobs_key='apscheduler.jobs', 
                    run_times_key='apscheduler.run_times', 
                    host='localhost',
                    port=6379,
                    db=0,
                    password=settings.REDIS_PASSWORD.get_secret_value(),
                )
            }
            executors = {
                'default': AsyncIOExecutor()
            }
            job_defaults = {
                'coalesce': True,
                'max_instances': 3
            }
            
            self.scheduler = AsyncIOScheduler(
                timezone="Europe/Moscow",
                jobstores=jobstores,
                executors=executors,
                job_defaults=job_defaults
            )
            
            logger.success("Планировщик успешно инициализирован")
            logger.debug(f"Jobstore: Redis, executors: AsyncIO, timezone: Europe/Moscow")
            
        except Exception as e:
            logger.error(f"Не удалось инициализировать планировщик: {e}")
            logger.opt(exception=True).debug("Подробности ошибки инициализации:")

    async def start_sc(self):
        """Запуск планировщика"""
        try:
            self.scheduler.start()
            logger.info("▶️ Планировщик задач запущен")
            
            # Логируем информацию о запланированных задачах
            jobs = self.scheduler.get_jobs()
            logger.info(f"Активных задач в планировщике: {len(jobs)}")
            
            for job in jobs:
                logger.debug(f"Задача: {job.id}, следующее выполнение: {job.next_run_time}")
                
        except Exception as e:
            logger.error(f"Ошибка при запуске планировщика: {e}")

    def scheduled_task(func):
        """Декоратор для планирования задач"""
        def wrapper(self, pit, **kwargs):
            try:
                job_id = f"{func.__name__}_{pit.name}_{kwargs.get('att')}"
                run_date = getattr(pit, kwargs.get('att'))
                
                self.scheduler.add_job(
                    func,
                    trigger="date",
                    run_date=run_date,
                    id=job_id,
                    kwargs={"pet": pit, "self": self, "att": kwargs.get('att')}
                )
                
                logger.info(
                    f"Запланирована задача '{func.__name__}' для питомца '{pit.name}' "
                    f"на {run_date} (ID: {job_id})"
                )
                
            except AttributeError as e:
                logger.error(f"Ошибка атрибута при планировании {func.__name__}: {e}")
            except Exception as e:
                logger.error(f"Ошибка при планировании задачи {func.__name__}: {e}")
                
        return wrapper

    @scheduled_task
    async def crack(self, pet: Pitomec, **kwargs):
        """Трещина в яйце"""
        logger.info(f"Начало процесса появления трещины у питомца '{pet.name}'")
        
        try:
            await Pitomec.crack(pet)
            logger.debug(f"Статус трещины обновлен для '{pet.name}'")
            
            # Отправка сообщений владельцам
            owners = [pet.owner1, pet.owner2]
            success_count = 0
            
            for owner_id in owners:
                if owner_id:
                    try:
                        await bot.send_message(
                            chat_id=owner_id,
                            text=f"""Яйцо дало первые трещинки!🥚🥚🥚
Еще немного терпения — {pet.name} уже готов вылупиться.
Следи за обновлениями или проверь через /me"""
                        )
                        success_count += 1
                        logger.debug(f"Уведомление отправлено владельцу {owner_id}")
                    except Exception as e:
                        logger.warning(f"Не удалось отправить уведомление владельцу {owner_id}: {e}")
            
            logger.info(f"📨 Уведомления о трещине отправлены {success_count}/{len(owners)} владельцам")
            
            # Планируем следующую задачу
            self.hatch(pet, att="time_to_hatch")
            logger.debug(f"Запланирован вылупление для '{pet.name}'")
            
        except Exception as e:
            logger.error(f"Ошибка в процессе crack для '{pet.name}': {e}")
            logger.opt(exception=True).debug("Подробности ошибки:")

    @scheduled_task
    async def hatch(self, pet: Pitomec, **kwargs):
        """Вылупление питомца"""
        logger.info(f"Начало процесса вылупления питомца '{pet.name}'")
        
        try:
            await Pitomec.hatch(pet)
            logger.debug(f"Статус вылупления обновлен для '{pet.name}'")
            
            # Получение и отправка изображения
            image = await Pitomec.get_image(pet)
            logger.debug(f"Получено изображение для '{pet.name}'")
            
            owners = [pet.owner1, pet.owner2]
            success_count = 0
            
            for owner_id in owners:
                if owner_id:
                    try:
                        await bot.send_photo(
                            chat_id=owner_id,
                            photo=image,
                            caption=f"""{pet.name} вылупился!🎉🎉🎉
Поздравляем! Теперь ваш новый друг рядом.
Он может загрустить без внимания"""
                        )
                        success_count += 1
                        logger.debug(f"Фото уведомление отправлено владельцу {owner_id}")
                    except Exception as e:
                        logger.warning(f"Не удалось отправить фото уведомление владельцу {owner_id}: {e}")
            
            logger.info(f"Уведомления о вылуплении отправлены {success_count}/{len(owners)} владельцам")
            
            # Установка начальных состояний
            await Pitomec.unhappy(pet)
            self.unhappy(pet, att="time_to_unhappy")
            logger.debug("Установлено состояние 'unhappy'")
            
            await Pitomec.hungry(pet)
            self.hungry(pet, att="time_to_hungry")
            logger.debug("Установлено состояние 'hungry'")
            
            await Pitomec.walk(pet)
            self.walk(pet, att="time_to_walk")
            logger.debug("Установлено состояние 'walk'")
            
            # Обновление в БД
            await DAO.upd(pet)
            logger.debug(f"Данные питомца '{pet.name}' обновлены в БД")
            
            logger.success(f"Питомец '{pet.name}' успешно вылупился и настроены все состояния")
            
        except Exception as e:
            logger.error(f"Ошибка в процессе hatch для '{pet.name}': {e}")
            logger.opt(exception=True).debug("Подробности ошибки:")

    @scheduled_task
    async def unhappy(self, pet: Pitomec, **kwargs):
        """Питомец грустит"""
        logger.info(f"Питомец '{pet.name}' начинает грустить")
        
        try:
            await Pitomec.change_mood(pet, "unhappy")
            logger.debug(f"Настроение изменено на 'unhappy' для '{pet.name}'")
            
            owners = [pet.owner1, pet.owner2]
            success_count = 0
            
            for owner_id in owners:
                if owner_id:
                    try:
                        await bot.send_message(
                            chat_id=owner_id,
                            text=f"{pet.name} грустит.....\n поиграй с ним",
                            reply_markup=to_be_happy_btn
                        )
                        success_count += 1
                        logger.debug(f"Уведомление о грусти отправлено владельцу {owner_id}")
                    except Exception as e:
                        logger.warning(f"Не удалось отправить уведомление о грусти владельцу {owner_id}: {e}")
            
            logger.info(f"Уведомления о грусти отправлены {success_count}/{len(owners)} владельцам")
            
        except Exception as e:
            logger.error(f"Ошибка в процессе unhappy для '{pet.name}': {e}")

    @scheduled_task
    async def hungry(self, pet: Pitomec, **kwargs):
        """Питомец голоден"""
        logger.info(f"Питомец '{pet.name}' проголодался")
        
        try:
            await Pitomec.change_mood(pet, "hungry")
            logger.debug(f"Настроение изменено на 'hungry' для '{pet.name}'")
            
            keyboard = hungry_bttn()
            owners = [pet.owner1, pet.owner2]
            success_count = 0
            
            for owner_id in owners:
                if owner_id:
                    try:
                        await bot.send_message(
                            chat_id=owner_id,
                            text=f"{pet.name} голоден.....\n покорми его",
                            reply_markup=keyboard
                        )
                        success_count += 1
                        logger.debug(f"Уведомление о голоде отправлено владельцу {owner_id}")
                    except Exception as e:
                        logger.warning(f"Не удалось отправить уведомление о голоде владельцу {owner_id}: {e}")
            
            logger.info(f"Уведомления о голоде отправлены {success_count}/{len(owners)} владельцам")
            
        except Exception as e:
            logger.error(f"Ошибка в процессе hungry для '{pet.name}': {e}")

    @scheduled_task
    async def walk(self, pet: Pitomec, **kwargs):
        """Питомец хочет гулять"""
        logger.info(f"Питомец '{pet.name}' хочет на прогулку")
        
        try:
            await Pitomec.change_mood(pet, "walk")
            logger.debug(f"Настроение изменено на 'walk' для '{pet.name}'")
            
            keyboard = walk_bttn()
            owners = [pet.owner1, pet.owner2]
            success_count = 0
            
            for owner_id in owners:
                if owner_id:
                    try:
                        await bot.send_message(
                            chat_id=owner_id,
                            text=f"{pet.name} хочет погулять.....\n выведи его на улицу",
                            reply_markup=keyboard
                        )
                        success_count += 1
                        logger.debug(f"Уведомление о прогулке отправлено владельцу {owner_id}")
                    except Exception as e:
                        logger.warning(f"Не удалось отправить уведомление о прогулке владельцу {owner_id}: {e}")
            
            logger.info(f"Уведомления о прогулке отправлены {success_count}/{len(owners)} владельцам")
            
        except Exception as e:
            logger.error(f"Ошибка в процессе walk для '{pet.name}': {e}")

# Глобальный экземпляр планировщика
scheduler = None
def ini_scheduler():
    global scheduler
    scheduler = C_scheduler()
    logger.debug("Создан глобальный экземпляр планировщика")